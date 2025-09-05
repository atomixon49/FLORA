import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
  Clipboard,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import Icon from 'react-native-vector-icons/MaterialIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';

const DecryptScreen: React.FC = () => {
  const [encryptedText, setEncryptedText] = useState('');
  const [decryptedText, setDecryptedText] = useState('');
  const [isDecrypting, setIsDecrypting] = useState(false);
  const [password, setPassword] = useState('');

  const simulateDecryption = async (encrypted: string, key: string): Promise<string> => {
    // Simulación de desifrado (en un entorno real, usaría el motor Rust)
    if (!encrypted.startsWith('FLORA:')) {
      throw new Error('Formato de texto cifrado inválido');
    }

    const hexData = encrypted.substring(6); // Remover 'FLORA:'
    const encryptedBytes = new Uint8Array(hexData.length / 2);
    
    for (let i = 0; i < hexData.length; i += 2) {
      encryptedBytes[i / 2] = parseInt(hexData.substr(i, 2), 16);
    }

    const keyBytes = new TextEncoder().encode(key);
    const decrypted = new Uint8Array(encryptedBytes.length);
    
    for (let i = 0; i < encryptedBytes.length; i++) {
      decrypted[i] = encryptedBytes[i] ^ keyBytes[i % keyBytes.length];
    }
    
    return new TextDecoder().decode(decrypted);
  };

  const handleDecrypt = async () => {
    if (!encryptedText.trim()) {
      Alert.alert('Error', 'Por favor ingresa el texto cifrado');
      return;
    }

    if (!password.trim()) {
      Alert.alert('Error', 'Por favor ingresa la contraseña');
      return;
    }

    setIsDecrypting(true);
    
    try {
      const decrypted = await simulateDecryption(encryptedText, password);
      setDecryptedText(decrypted);
      
      // Guardar estadísticas
      const totalSessions = await AsyncStorage.getItem('totalSessions');
      const count = totalSessions ? parseInt(totalSessions) + 1 : 1;
      await AsyncStorage.setItem('totalSessions', count.toString());
      await AsyncStorage.setItem('lastActivity', new Date().toISOString());
      
      Alert.alert('Éxito', 'Texto desifrado correctamente');
    } catch (error) {
      Alert.alert('Error', 'Error al desifrar. Verifica la contraseña y el formato del texto.');
    } finally {
      setIsDecrypting(false);
    }
  };

  const handlePaste = async () => {
    try {
      const text = await Clipboard.getString();
      setEncryptedText(text);
    } catch (error) {
      Alert.alert('Error', 'No se pudo acceder al portapapeles');
    }
  };

  const handleCopyDecrypted = () => {
    Clipboard.setString(decryptedText);
    Alert.alert('Copiado', 'Texto desifrado copiado al portapapeles');
  };

  const handleClear = () => {
    setEncryptedText('');
    setDecryptedText('');
    setPassword('');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        {/* Password Input */}
        <View style={styles.inputContainer}>
          <Text style={styles.label}>Contraseña de Desifrado</Text>
          <TextInput
            style={styles.passwordInput}
            value={password}
            onChangeText={setPassword}
            placeholder="Ingresa la contraseña usada para cifrar"
            secureTextEntry
            autoCapitalize="none"
          />
        </View>

        {/* Encrypted Text Input */}
        <View style={styles.inputContainer}>
          <View style={styles.labelContainer}>
            <Text style={styles.label}>Texto Cifrado</Text>
            <TouchableOpacity
              style={styles.pasteButton}
              onPress={handlePaste}
            >
              <Icon name="content-paste" size={16} color="#2196F3" />
              <Text style={styles.pasteButtonText}>Pegar</Text>
            </TouchableOpacity>
          </View>
          <TextInput
            style={styles.textInput}
            value={encryptedText}
            onChangeText={setEncryptedText}
            placeholder="Pega aquí el texto cifrado (formato FLORA:...)"
            multiline
            numberOfLines={6}
            textAlignVertical="top"
          />
        </View>

        {/* Action Buttons */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, styles.decryptButton]}
            onPress={handleDecrypt}
            disabled={isDecrypting}
          >
            <LinearGradient
              colors={['#2196F3', '#1976D2']}
              style={styles.buttonGradient}
            >
              <Icon name="lock-open" size={20} color="#ffffff" />
              <Text style={styles.buttonText}>
                {isDecrypting ? 'Desifrando...' : 'Desifrar Texto'}
              </Text>
            </LinearGradient>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.clearButton]}
            onPress={handleClear}
          >
            <Icon name="clear" size={20} color="#666" />
            <Text style={[styles.buttonText, styles.clearButtonText]}>Limpiar</Text>
          </TouchableOpacity>
        </View>

        {/* Decrypted Result */}
        {decryptedText ? (
          <View style={styles.resultContainer}>
            <View style={styles.resultHeader}>
              <Text style={styles.resultLabel}>Texto Desifrado:</Text>
              <TouchableOpacity
                style={styles.copyButton}
                onPress={handleCopyDecrypted}
              >
                <Icon name="content-copy" size={20} color="#2196F3" />
                <Text style={styles.copyButtonText}>Copiar</Text>
              </TouchableOpacity>
            </View>
            <View style={styles.resultBox}>
              <Text style={styles.resultText}>{decryptedText}</Text>
            </View>
          </View>
        ) : null}

        {/* Security Warning */}
        <View style={styles.warningContainer}>
          <Icon name="warning" size={20} color="#FF9800" />
          <View style={styles.warningContent}>
            <Text style={styles.warningTitle}>Advertencia de Seguridad</Text>
            <Text style={styles.warningText}>
              • Solo desifra textos que hayas cifrado tú{'\n'}
              • Verifica que la contraseña sea correcta{'\n'}
              • No compartas contraseñas por mensajes{'\n'}
              • Los datos se procesan localmente
            </Text>
          </View>
        </View>

        {/* Quick Help */}
        <View style={styles.helpContainer}>
          <Icon name="help" size={20} color="#4CAF50" />
          <View style={styles.helpContent}>
            <Text style={styles.helpTitle}>Ayuda Rápida</Text>
            <Text style={styles.helpText}>
              • El texto cifrado debe comenzar con "FLORA:"{'\n'}
              • Usa la misma contraseña que usaste para cifrar{'\n'}
              • Puedes pegar texto desde el portapapeles{'\n'}
              • El resultado se puede copiar fácilmente
            </Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    padding: 20,
  },
  inputContainer: {
    marginBottom: 20,
  },
  labelContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  pasteButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#e3f2fd',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  pasteButtonText: {
    marginLeft: 4,
    fontSize: 12,
    color: '#2196F3',
    fontWeight: '500',
  },
  passwordInput: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  textInput: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    minHeight: 120,
    fontFamily: 'monospace',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  button: {
    flex: 1,
    marginHorizontal: 5,
    borderRadius: 8,
    overflow: 'hidden',
  },
  decryptButton: {
    flex: 2,
  },
  clearButton: {
    backgroundColor: '#f0f0f0',
    padding: 12,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
  },
  buttonGradient: {
    padding: 15,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  clearButtonText: {
    color: '#666',
  },
  resultContainer: {
    backgroundColor: '#ffffff',
    borderRadius: 8,
    padding: 15,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  resultLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  copyButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#e3f2fd',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  copyButtonText: {
    marginLeft: 4,
    fontSize: 12,
    color: '#2196F3',
    fontWeight: '500',
  },
  resultBox: {
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#e9ecef',
    borderRadius: 6,
    padding: 12,
  },
  resultText: {
    fontSize: 16,
    color: '#495057',
    lineHeight: 24,
  },
  warningContainer: {
    flexDirection: 'row',
    backgroundColor: '#fff3e0',
    padding: 15,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#FF9800',
    marginBottom: 15,
  },
  warningContent: {
    marginLeft: 10,
    flex: 1,
  },
  warningTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#f57c00',
    marginBottom: 5,
  },
  warningText: {
    fontSize: 12,
    color: '#f57c00',
    lineHeight: 16,
  },
  helpContainer: {
    flexDirection: 'row',
    backgroundColor: '#e8f5e8',
    padding: 15,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#4CAF50',
  },
  helpContent: {
    marginLeft: 10,
    flex: 1,
  },
  helpTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#388e3c',
    marginBottom: 5,
  },
  helpText: {
    fontSize: 12,
    color: '#388e3c',
    lineHeight: 16,
  },
});

export default DecryptScreen;

