import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import Icon from 'react-native-vector-icons/MaterialIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';

const SecurityScreen: React.FC = () => {
  const [securitySettings, setSecuritySettings] = useState({
    biometricAuth: false,
    autoLock: true,
    secureMode: true,
    dataEncryption: true,
    auditLog: true,
  });
  const [securityScore, setSecurityScore] = useState(0);
  const [threats, setThreats] = useState<string[]>([]);

  useEffect(() => {
    loadSecuritySettings();
    calculateSecurityScore();
  }, []);

  const loadSecuritySettings = async () => {
    try {
      const settings = await AsyncStorage.getItem('securitySettings');
      if (settings) {
        setSecuritySettings(JSON.parse(settings));
      }
    } catch (error) {
      console.error('Error loading security settings:', error);
    }
  };

  const saveSecuritySettings = async (newSettings: typeof securitySettings) => {
    try {
      await AsyncStorage.setItem('securitySettings', JSON.stringify(newSettings));
      setSecuritySettings(newSettings);
      calculateSecurityScore();
    } catch (error) {
      console.error('Error saving security settings:', error);
    }
  };

  const calculateSecurityScore = () => {
    let score = 0;
    const newThreats: string[] = [];

    if (securitySettings.biometricAuth) score += 25;
    else newThreats.push('Autenticación biométrica deshabilitada');

    if (securitySettings.autoLock) score += 20;
    else newThreats.push('Bloqueo automático deshabilitado');

    if (securitySettings.secureMode) score += 25;
    else newThreats.push('Modo seguro deshabilitado');

    if (securitySettings.dataEncryption) score += 20;
    else newThreats.push('Cifrado de datos deshabilitado');

    if (securitySettings.auditLog) score += 10;
    else newThreats.push('Registro de auditoría deshabilitado');

    setSecurityScore(score);
    setThreats(newThreats);
  };

  const toggleSetting = (setting: keyof typeof securitySettings) => {
    const newSettings = {
      ...securitySettings,
      [setting]: !securitySettings[setting],
    };
    saveSecuritySettings(newSettings);
  };

  const getSecurityLevel = () => {
    if (securityScore >= 80) return { level: 'Excelente', color: '#4CAF50' };
    if (securityScore >= 60) return { level: 'Bueno', color: '#FF9800' };
    if (securityScore >= 40) return { level: 'Regular', color: '#FF5722' };
    return { level: 'Crítico', color: '#f44336' };
  };

  const SecurityCard = ({ 
    title, 
    description, 
    icon, 
    enabled, 
    onToggle, 
    color = '#667eea' 
  }: {
    title: string;
    description: string;
    icon: string;
    enabled: boolean;
    onToggle: () => void;
    color?: string;
  }) => (
    <View style={styles.securityCard}>
      <View style={styles.cardHeader}>
        <View style={[styles.iconContainer, { backgroundColor: color + '20' }]}>
          <Icon name={icon} size={24} color={color} />
        </View>
        <View style={styles.cardInfo}>
          <Text style={styles.cardTitle}>{title}</Text>
          <Text style={styles.cardDescription}>{description}</Text>
        </View>
        <Switch
          value={enabled}
          onValueChange={onToggle}
          trackColor={{ false: '#f0f0f0', true: color }}
          thumbColor={enabled ? '#ffffff' : '#f4f3f4'}
        />
      </View>
    </View>
  );

  const ThreatItem = ({ threat }: { threat: string }) => (
    <View style={styles.threatItem}>
      <Icon name="warning" size={16} color="#f44336" />
      <Text style={styles.threatText}>{threat}</Text>
    </View>
  );

  const securityLevel = getSecurityLevel();

  return (
    <ScrollView style={styles.container}>
      {/* Security Score Header */}
      <LinearGradient
        colors={[securityLevel.color, securityLevel.color + '80']}
        style={styles.scoreHeader}
      >
        <View style={styles.scoreContent}>
          <Text style={styles.scoreTitle}>Puntuación de Seguridad</Text>
          <Text style={styles.scoreValue}>{securityScore}/100</Text>
          <Text style={styles.scoreLevel}>{securityLevel.level}</Text>
        </View>
        <View style={styles.scoreCircle}>
          <Text style={styles.scoreCircleText}>{securityScore}%</Text>
        </View>
      </LinearGradient>

      {/* Security Settings */}
      <View style={styles.settingsContainer}>
        <Text style={styles.sectionTitle}>Configuración de Seguridad</Text>
        
        <SecurityCard
          title="Autenticación Biométrica"
          description="Usar huella dactilar o reconocimiento facial"
          icon="fingerprint"
          enabled={securitySettings.biometricAuth}
          onToggle={() => toggleSetting('biometricAuth')}
          color="#4CAF50"
        />

        <SecurityCard
          title="Bloqueo Automático"
          description="Bloquear la app después de inactividad"
          icon="lock-clock"
          enabled={securitySettings.autoLock}
          onToggle={() => toggleSetting('autoLock')}
          color="#2196F3"
        />

        <SecurityCard
          title="Modo Seguro"
          description="Cifrado adicional para datos sensibles"
          icon="security"
          enabled={securitySettings.secureMode}
          onToggle={() => toggleSetting('secureMode')}
          color="#9C27B0"
        />

        <SecurityCard
          title="Cifrado de Datos"
          description="Cifrar todos los datos almacenados"
          icon="enhanced-encryption"
          enabled={securitySettings.dataEncryption}
          onToggle={() => toggleSetting('dataEncryption')}
          color="#FF9800"
        />

        <SecurityCard
          title="Registro de Auditoría"
          description="Registrar todas las actividades de seguridad"
          icon="history"
          enabled={securitySettings.auditLog}
          onToggle={() => toggleSetting('auditLog')}
          color="#607D8B"
        />
      </View>

      {/* Security Threats */}
      {threats.length > 0 && (
        <View style={styles.threatsContainer}>
          <Text style={styles.sectionTitle}>Amenazas Detectadas</Text>
          {threats.map((threat, index) => (
            <ThreatItem key={index} threat={threat} />
          ))}
        </View>
      )}

      {/* Security Tips */}
      <View style={styles.tipsContainer}>
        <Text style={styles.sectionTitle}>Consejos de Seguridad</Text>
        
        <View style={styles.tipItem}>
          <Icon name="lightbulb" size={20} color="#FFC107" />
          <Text style={styles.tipText}>
            Usa contraseñas fuertes con al menos 12 caracteres
          </Text>
        </View>
        
        <View style={styles.tipItem}>
          <Icon name="lightbulb" size={20} color="#FFC107" />
          <Text style={styles.tipText}>
            Habilita la autenticación biométrica para mayor seguridad
          </Text>
        </View>
        
        <View style={styles.tipItem}>
          <Icon name="lightbulb" size={20} color="#FFC107" />
          <Text style={styles.tipText}>
            Mantén la app actualizada para obtener las últimas protecciones
          </Text>
        </View>
        
        <View style={styles.tipItem}>
          <Icon name="lightbulb" size={20} color="#FFC107" />
          <Text style={styles.tipText}>
            No compartas tus contraseñas por mensajes o email
          </Text>
        </View>
      </View>

      {/* Security Actions */}
      <View style={styles.actionsContainer}>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => Alert.alert('Información', 'Función de respaldo en desarrollo')}
        >
          <Icon name="backup" size={20} color="#ffffff" />
          <Text style={styles.actionButtonText}>Respaldar Datos</Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          style={[styles.actionButton, styles.secondaryButton]}
          onPress={() => Alert.alert('Información', 'Función de restauración en desarrollo')}
        >
          <Icon name="restore" size={20} color="#667eea" />
          <Text style={[styles.actionButtonText, { color: '#667eea' }]}>Restaurar Datos</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scoreHeader: {
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  scoreContent: {
    flex: 1,
  },
  scoreTitle: {
    fontSize: 16,
    color: '#ffffff',
    opacity: 0.9,
  },
  scoreValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffffff',
    marginTop: 5,
  },
  scoreLevel: {
    fontSize: 18,
    color: '#ffffff',
    opacity: 0.9,
    marginTop: 5,
  },
  scoreCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  scoreCircleText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  settingsContainer: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  securityCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 15,
  },
  cardInfo: {
    flex: 1,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  cardDescription: {
    fontSize: 14,
    color: '#666',
  },
  threatsContainer: {
    padding: 20,
    paddingTop: 0,
  },
  threatItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffebee',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#f44336',
  },
  threatText: {
    marginLeft: 10,
    fontSize: 14,
    color: '#d32f2f',
    flex: 1,
  },
  tipsContainer: {
    padding: 20,
    paddingTop: 0,
  },
  tipItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    backgroundColor: '#ffffff',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  tipText: {
    marginLeft: 10,
    fontSize: 14,
    color: '#333',
    flex: 1,
    lineHeight: 20,
  },
  actionsContainer: {
    padding: 20,
    paddingTop: 0,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#667eea',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
  },
  secondaryButton: {
    backgroundColor: '#f0f0f0',
  },
  actionButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
});

export default SecurityScreen;

