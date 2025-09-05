// FLORA Mobile App - Test Version
// Versión simplificada para pruebas rápidas

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ScrollView,
  Alert,
} from 'react-native';

const TestApp = () => {
  const [inputText, setInputText] = useState('');
  const [encryptedText, setEncryptedText] = useState('');
  const [password, setPassword] = useState('');

  const simulateEncryption = (text, key) => {
    // Simulación simple de cifrado
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

  const simulateDecryption = (encrypted, key) => {
    if (!encrypted.startsWith('FLORA:')) {
      throw new Error('Formato inválido');
    }

    const hexData = encrypted.substring(6);
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

  const handleEncrypt = () => {
    if (!inputText.trim() || !password.trim()) {
      Alert.alert('Error', 'Completa todos los campos');
      return;
    }

    try {
      const encrypted = simulateEncryption(inputText, password);
      setEncryptedText(encrypted);
      Alert.alert('Éxito', 'Texto cifrado correctamente');
    } catch (error) {
      Alert.alert('Error', 'Error al cifrar');
    }
  };

  const handleDecrypt = () => {
    if (!encryptedText.trim() || !password.trim()) {
      Alert.alert('Error', 'Completa todos los campos');
      return;
    }

    try {
      const decrypted = simulateDecryption(encryptedText, password);
      setInputText(decrypted);
      Alert.alert('Éxito', 'Texto desifrado correctamente');
    } catch (error) {
      Alert.alert('Error', 'Error al desifrar. Verifica la contraseña.');
    }
  };

  const handleClear = () => {
    setInputText('');
    setEncryptedText('');
    setPassword('');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🌸 FLORA Test</Text>
        <Text style={styles.subtitle}>Sistema de Cifrado Híbrido Post-Cuántico</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Contraseña</Text>
        <TextInput
          style={styles.input}
          value={password}
          onChangeText={setPassword}
          placeholder="Ingresa tu contraseña"
          secureTextEntry
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Texto a Cifrar/Desifrar</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Escribe tu texto aquí..."
          multiline
          numberOfLines={4}
        />
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity style={[styles.button, styles.encryptButton]} onPress={handleEncrypt}>
          <Text style={styles.buttonText}>🔐 Cifrar</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={[styles.button, styles.decryptButton]} onPress={handleDecrypt}>
          <Text style={styles.buttonText}>🔓 Desifrar</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Resultado</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          value={encryptedText}
          onChangeText={setEncryptedText}
          placeholder="El texto cifrado aparecerá aquí..."
          multiline
          numberOfLines={4}
        />
      </View>

      <TouchableOpacity style={[styles.button, styles.clearButton]} onPress={handleClear}>
        <Text style={[styles.buttonText, styles.clearButtonText]}>🗑️ Limpiar Todo</Text>
      </TouchableOpacity>

      <View style={styles.info}>
        <Text style={styles.infoTitle}>ℹ️ Información</Text>
        <Text style={styles.infoText}>
          • Esta es una versión de prueba{'\n'}
          • El cifrado es simulado para demostración{'\n'}
          • En producción se usaría el motor Rust de FLORA{'\n'}
          • Los datos se procesan localmente
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#667eea',
    padding: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: '#ffffff',
    opacity: 0.9,
  },
  section: {
    margin: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  input: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  textArea: {
    minHeight: 100,
    textAlignVertical: 'top',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    margin: 20,
  },
  button: {
    flex: 1,
    marginHorizontal: 5,
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  encryptButton: {
    backgroundColor: '#4CAF50',
  },
  decryptButton: {
    backgroundColor: '#2196F3',
  },
  clearButton: {
    backgroundColor: '#f44336',
    margin: 20,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  clearButtonText: {
    color: '#ffffff',
  },
  info: {
    backgroundColor: '#e3f2fd',
    margin: 20,
    padding: 15,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#2196F3',
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1976d2',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 14,
    color: '#1976d2',
    lineHeight: 20,
  },
});

export default TestApp;

