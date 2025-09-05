import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Dimensions,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { useNavigation } from '@react-navigation/native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width } = Dimensions.get('window');

interface FloraStats {
  encryptedFiles: number;
  totalSessions: number;
  securityLevel: number;
  lastActivity: string;
}

const HomeScreen: React.FC = () => {
  const navigation = useNavigation();
  const [stats, setStats] = useState<FloraStats>({
    encryptedFiles: 0,
    totalSessions: 0,
    securityLevel: 0,
    lastActivity: 'Nunca',
  });
  const [isSecure, setIsSecure] = useState(false);

  useEffect(() => {
    loadStats();
    checkSecurityStatus();
  }, []);

  const loadStats = async () => {
    try {
      const encryptedFiles = await AsyncStorage.getItem('encryptedFiles');
      const totalSessions = await AsyncStorage.getItem('totalSessions');
      const lastActivity = await AsyncStorage.getItem('lastActivity');
      
      setStats({
        encryptedFiles: encryptedFiles ? parseInt(encryptedFiles) : 0,
        totalSessions: totalSessions ? parseInt(totalSessions) : 0,
        securityLevel: 85, // Simulado
        lastActivity: lastActivity || 'Nunca',
      });
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const checkSecurityStatus = async () => {
    try {
      const masterKey = await AsyncStorage.getItem('masterKey');
      setIsSecure(!!masterKey);
    } catch (error) {
      console.error('Error checking security:', error);
    }
  };

  const handleQuickAction = (action: string) => {
    switch (action) {
      case 'encrypt':
        navigation.navigate('Encrypt' as never);
        break;
      case 'decrypt':
        navigation.navigate('Decrypt' as never);
        break;
      case 'files':
        navigation.navigate('Files' as never);
        break;
      case 'security':
        navigation.navigate('Security' as never);
        break;
    }
  };

  const QuickActionButton = ({ 
    icon, 
    title, 
    subtitle, 
    onPress, 
    color 
  }: {
    icon: string;
    title: string;
    subtitle: string;
    onPress: () => void;
    color: string;
  }) => (
    <TouchableOpacity style={styles.quickAction} onPress={onPress}>
      <LinearGradient
        colors={[color, color + '80']}
        style={styles.quickActionGradient}
      >
        <Icon name={icon} size={32} color="#ffffff" />
        <Text style={styles.quickActionTitle}>{title}</Text>
        <Text style={styles.quickActionSubtitle}>{subtitle}</Text>
      </LinearGradient>
    </TouchableOpacity>
  );

  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <LinearGradient
        colors={['#667eea', '#764ba2']}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <Text style={styles.headerTitle}>🌸 FLORA</Text>
          <Text style={styles.headerSubtitle}>Cifrado Híbrido Post-Cuántico</Text>
          <View style={styles.securityStatus}>
            <Icon 
              name={isSecure ? "security" : "security"} 
              size={20} 
              color={isSecure ? "#4CAF50" : "#FF9800"} 
            />
            <Text style={[styles.securityText, { color: isSecure ? "#4CAF50" : "#FF9800" }]}>
              {isSecure ? "Sistema Seguro" : "Configuración Requerida"}
            </Text>
          </View>
        </View>
      </LinearGradient>

      {/* Quick Actions */}
      <View style={styles.quickActionsContainer}>
        <Text style={styles.sectionTitle}>Acciones Rápidas</Text>
        <View style={styles.quickActionsGrid}>
          <QuickActionButton
            icon="lock"
            title="Cifrar"
            subtitle="Proteger datos"
            onPress={() => handleQuickAction('encrypt')}
            color="#4CAF50"
          />
          <QuickActionButton
            icon="lock-open"
            title="Desifrar"
            subtitle="Recuperar datos"
            onPress={() => handleQuickAction('decrypt')}
            color="#2196F3"
          />
          <QuickActionButton
            icon="folder"
            title="Archivos"
            subtitle="Gestionar archivos"
            onPress={() => handleQuickAction('files')}
            color="#FF9800"
          />
          <QuickActionButton
            icon="security"
            title="Seguridad"
            subtitle="Centro de control"
            onPress={() => handleQuickAction('security')}
            color="#9C27B0"
          />
        </View>
      </View>

      {/* Statistics */}
      <View style={styles.statsContainer}>
        <Text style={styles.sectionTitle}>Estadísticas</Text>
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <Icon name="lock" size={24} color="#4CAF50" />
            <Text style={styles.statNumber}>{stats.encryptedFiles}</Text>
            <Text style={styles.statLabel}>Archivos Cifrados</Text>
          </View>
          <View style={styles.statCard}>
            <Icon name="history" size={24} color="#2196F3" />
            <Text style={styles.statNumber}>{stats.totalSessions}</Text>
            <Text style={styles.statLabel}>Sesiones</Text>
          </View>
          <View style={styles.statCard}>
            <Icon name="security" size={24} color="#FF9800" />
            <Text style={styles.statNumber}>{stats.securityLevel}%</Text>
            <Text style={styles.statLabel}>Nivel Seguridad</Text>
          </View>
          <View style={styles.statCard}>
            <Icon name="schedule" size={24} color="#9C27B0" />
            <Text style={styles.statNumber}>-</Text>
            <Text style={styles.statLabel}>Última Actividad</Text>
          </View>
        </View>
      </View>

      {/* Recent Activity */}
      <View style={styles.recentContainer}>
        <Text style={styles.sectionTitle}>Actividad Reciente</Text>
        <View style={styles.recentItem}>
          <Icon name="lock" size={20} color="#4CAF50" />
          <View style={styles.recentContent}>
            <Text style={styles.recentTitle}>Archivo cifrado</Text>
            <Text style={styles.recentSubtitle}>documento_secreto.txt</Text>
            <Text style={styles.recentTime}>Hace 2 horas</Text>
          </View>
        </View>
        <View style={styles.recentItem}>
          <Icon name="lock-open" size={20} color="#2196F3" />
          <View style={styles.recentContent}>
            <Text style={styles.recentTitle}>Archivo desifrado</Text>
            <Text style={styles.recentSubtitle}>imagen_privada.jpg</Text>
            <Text style={styles.recentTime}>Hace 1 día</Text>
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
  header: {
    padding: 20,
    paddingTop: 40,
    paddingBottom: 30,
  },
  headerContent: {
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 5,
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#ffffff',
    opacity: 0.9,
    marginBottom: 15,
  },
  securityStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
  },
  securityText: {
    marginLeft: 8,
    fontWeight: '600',
  },
  quickActionsContainer: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  quickAction: {
    width: (width - 60) / 2,
    marginBottom: 15,
    borderRadius: 12,
    overflow: 'hidden',
  },
  quickActionGradient: {
    padding: 20,
    alignItems: 'center',
    borderRadius: 12,
  },
  quickActionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
    marginTop: 10,
  },
  quickActionSubtitle: {
    fontSize: 12,
    color: '#ffffff',
    opacity: 0.9,
    marginTop: 5,
  },
  statsContainer: {
    padding: 20,
    paddingTop: 0,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statCard: {
    width: (width - 60) / 2,
    backgroundColor: '#ffffff',
    padding: 15,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  recentContainer: {
    padding: 20,
    paddingTop: 0,
  },
  recentItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  recentContent: {
    marginLeft: 15,
    flex: 1,
  },
  recentTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  recentSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  recentTime: {
    fontSize: 12,
    color: '#999',
    marginTop: 2,
  },
});

export default HomeScreen;

