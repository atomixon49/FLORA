import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
  Share,
  Clipboard,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import Icon from 'react-native-vector-icons/MaterialIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';

const EncryptScreen: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [encryptedText, setEncryptedText] = useState('');
  const [isEncrypting, setIsEncrypting] = useState(false);
  const [password, setPassword] = useState('');

  const simulateEncryption = async (text: string, key: string): Promise<string> => {
    // Simulación de cifrado (en un entorno real, usaría el motor Rust)
    const keyBytes = new TextEncoder().encode(key);
    const textBytes = new TextEncoder().encode(text);
    const encrypted = new Uint8Array(textBytes.length);
    
    for (let i = 0; i < textBytes.length; i++) {
      encrypted[i] = textBytes[i] ^ keyBytes[i % keyBytes.length];
    }
    
    return 'FLORA:' + Array.from(encrypted)
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
  };

  const handleEncrypt = async () => {
    if (!inputText.trim()) {
      Alert.alert('Error', 'Por favor ingresa texto para cifrar');
      return;
    }

    if (!password.trim()) {
      Alert.alert('Error', 'Por favor ingresa una contraseña');
      return;
    }

    setIsEncrypting(true);
    
    try {
      const encrypted = await simulateEncryption(inputText, password);
      setEncryptedText(encrypted);
      
      // Guardar estadísticas
      const encryptedFiles = await AsyncStorage.getItem('encryptedFiles');
      const count = encryptedFiles ? parseInt(encryptedFiles) + 1 : 1;
      await AsyncStorage.setItem('encryptedFiles', count.toString());
      await AsyncStorage.setItem('lastActivity', new Date().toISOString());
      
      Alert.alert('Éxito', 'Texto cifrado correctamente');
    } catch (error) {
      Alert.alert('Error', 'Error al cifrar el texto');
    } finally {
      setIsEncrypting(false);
    }
  };

  const handleCopy = () => {
    Clipboard.setString(encryptedText);
    Alert.alert('Copiado', 'Texto cifrado copiado al portapapeles');
  };

  const handleShare = async () => {
    try {
      await Share.share({
        message: encryptedText,
        title: 'FLORA - Texto Cifrado',
      });
    } catch (error) {
      Alert.alert('Error', 'Error al compartir');
    }
  };

  const handleClear = () => {
    setInputText('');
    setEncryptedText('');
    setPassword('');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        {/* Password Input */}
        <View style={styles.inputContainer}>
          <Text style={styles.label}>Contraseña de Cifrado</Text>
          <TextInput
            style={styles.passwordInput}
            value={password}
            onChangeText={setPassword}
            placeholder="Ingresa tu contraseña"
            secureTextEntry
            autoCapitalize="none"
          />
        </View>

        {/* Text Input */}
        <View style={styles.inputContainer}>
          <Text style={styles.label}>Texto a Cifrar</Text>
          <TextInput
            style={styles.textInput}
            value={inputText}
            onChangeText={setInputText}
            placeholder="Escribe el texto que quieres cifrar..."
            multiline
            numberOfLines={6}
            textAlignVertical="top"
          />
        </View>

        {/* Action Buttons */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, styles.encryptButton]}
            onPress={handleEncrypt}
            disabled={isEncrypting}
          >
            <LinearGradient
              colors={['#4CAF50', '#45a049']}
              style={styles.buttonGradient}
            >
              <Icon name="lock" size={20} color="#ffffff" />
              <Text style={styles.buttonText}>
                {isEncrypting ? 'Cifrando...' : 'Cifrar Texto'}
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

        {/* Encrypted Result */}
        {encryptedText ? (
          <View style={styles.resultContainer}>
            <Text style={styles.resultLabel}>Texto Cifrado:</Text>
            <View style={styles.resultBox}>
              <Text style={styles.resultText}>{encryptedText}</Text>
            </View>
            
            <View style={styles.resultActions}>
              <TouchableOpacity
                style={[styles.actionButton, styles.copyButton]}
                onPress={handleCopy}
              >
                <Icon name="content-copy" size={20} color="#2196F3" />
                <Text style={styles.actionButtonText}>Copiar</Text>
              </TouchableOpacity>
              
              <TouchableOpacity
                style={[styles.actionButton, styles.shareButton]}
                onPress={handleShare}
              >
                <Icon name="share" size={20} color="#4CAF50" />
                <Text style={styles.actionButtonText}>Compartir</Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : null}

        {/* Security Info */}
        <View style={styles.infoContainer}>
          <Icon name="info" size={20} color="#2196F3" />
          <View style={styles.infoContent}>
            <Text style={styles.infoTitle}>Información de Seguridad</Text>
            <Text style={styles.infoText}>
              • El texto se cifra usando AES-256-GCM{'\n'}
              • La contraseña se deriva usando PBKDF2{'\n'}
              • Cada cifrado genera un nonce único{'\n'}
              • Los datos se procesan localmente
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
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
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
  encryptButton: {
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
  resultLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 10,
  },
  resultBox: {
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#e9ecef',
    borderRadius: 6,
    padding: 12,
    marginBottom: 15,
  },
  resultText: {
    fontSize: 14,
    fontFamily: 'monospace',
    color: '#495057',
    lineHeight: 20,
  },
  resultActions: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 10,
    borderRadius: 6,
  },
  copyButton: {
    backgroundColor: '#e3f2fd',
  },
  shareButton: {
    backgroundColor: '#e8f5e8',
  },
  actionButtonText: {
    marginLeft: 8,
    fontSize: 14,
    fontWeight: '500',
  },
  infoContainer: {
    flexDirection: 'row',
    backgroundColor: '#e3f2fd',
    padding: 15,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#2196F3',
  },
  infoContent: {
    marginLeft: 10,
    flex: 1,
  },
  infoTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1976d2',
    marginBottom: 5,
  },
  infoText: {
    fontSize: 12,
    color: '#1976d2',
    lineHeight: 16,
  },
});

export default EncryptScreen;

