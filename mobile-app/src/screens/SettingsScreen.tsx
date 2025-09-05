import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
  Linking,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';

const SettingsScreen: React.FC = () => {
  const [settings, setSettings] = useState({
    darkMode: false,
    notifications: true,
    autoSync: true,
    language: 'es',
    theme: 'default',
  });
  const [appVersion, setAppVersion] = useState('1.0.0');

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const savedSettings = await AsyncStorage.getItem('appSettings');
      if (savedSettings) {
        setSettings(JSON.parse(savedSettings));
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  };

  const saveSettings = async (newSettings: typeof settings) => {
    try {
      await AsyncStorage.setItem('appSettings', JSON.stringify(newSettings));
      setSettings(newSettings);
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  };

  const toggleSetting = (setting: keyof typeof settings) => {
    const newSettings = {
      ...settings,
      [setting]: !settings[setting],
    };
    saveSettings(newSettings);
  };

  const handleLanguageChange = () => {
    Alert.alert(
      'Idioma',
      'Selecciona tu idioma preferido',
      [
        { text: 'Español', onPress: () => updateSetting('language', 'es') },
        { text: 'English', onPress: () => updateSetting('language', 'en') },
        { text: 'Français', onPress: () => updateSetting('language', 'fr') },
        { text: 'Cancelar', style: 'cancel' },
      ]
    );
  };

  const handleThemeChange = () => {
    Alert.alert(
      'Tema',
      'Selecciona el tema de la aplicación',
      [
        { text: 'Por defecto', onPress: () => updateSetting('theme', 'default') },
        { text: 'Oscuro', onPress: () => updateSetting('theme', 'dark') },
        { text: 'Azul', onPress: () => updateSetting('theme', 'blue') },
        { text: 'Verde', onPress: () => updateSetting('theme', 'green') },
        { text: 'Cancelar', style: 'cancel' },
      ]
    );
  };

  const updateSetting = (key: keyof typeof settings, value: any) => {
    const newSettings = { ...settings, [key]: value };
    saveSettings(newSettings);
  };

  const handleClearData = () => {
    Alert.alert(
      'Limpiar Datos',
      '¿Estás seguro de que quieres eliminar todos los datos de la aplicación? Esta acción no se puede deshacer.',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Eliminar',
          style: 'destructive',
          onPress: () => {
            AsyncStorage.clear();
            Alert.alert('Éxito', 'Datos eliminados correctamente');
          },
        },
      ]
    );
  };

  const handleExportData = () => {
    Alert.alert('Exportar Datos', 'Función de exportación en desarrollo');
  };

  const handleContactSupport = () => {
    Alert.alert(
      'Soporte',
      '¿Cómo quieres contactar al soporte?',
      [
        { text: 'Email', onPress: () => Linking.openURL('mailto:support@flora.app') },
        { text: 'Sitio Web', onPress: () => Linking.openURL('https://flora.app/support') },
        { text: 'Cancelar', style: 'cancel' },
      ]
    );
  };

  const SettingItem = ({ 
    icon, 
    title, 
    subtitle, 
    onPress, 
    rightElement, 
    color = '#667eea' 
  }: {
    icon: string;
    title: string;
    subtitle?: string;
    onPress?: () => void;
    rightElement?: React.ReactNode;
    color?: string;
  }) => (
    <TouchableOpacity
      style={styles.settingItem}
      onPress={onPress}
      disabled={!onPress}
    >
      <View style={[styles.iconContainer, { backgroundColor: color + '20' }]}>
        <Icon name={icon} size={24} color={color} />
      </View>
      <View style={styles.settingInfo}>
        <Text style={styles.settingTitle}>{title}</Text>
        {subtitle && <Text style={styles.settingSubtitle}>{subtitle}</Text>}
      </View>
      {rightElement || (onPress && <Icon name="chevron-right" size={24} color="#ccc" />)}
    </TouchableOpacity>
  );

  const getLanguageName = (code: string) => {
    const languages: { [key: string]: string } = {
      es: 'Español',
      en: 'English',
      fr: 'Français',
    };
    return languages[code] || code;
  };

  const getThemeName = (theme: string) => {
    const themes: { [key: string]: string } = {
      default: 'Por defecto',
      dark: 'Oscuro',
      blue: 'Azul',
      green: 'Verde',
    };
    return themes[theme] || theme;
  };

  return (
    <ScrollView style={styles.container}>
      {/* App Info */}
      <View style={styles.appInfoContainer}>
        <View style={styles.appIcon}>
          <Text style={styles.appIconText}>🌸</Text>
        </View>
        <Text style={styles.appName}>FLORA</Text>
        <Text style={styles.appVersion}>Versión {appVersion}</Text>
        <Text style={styles.appDescription}>
          Sistema de Cifrado Híbrido Post-Cuántico
        </Text>
      </View>

      {/* General Settings */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>General</Text>
        
        <SettingItem
          icon="language"
          title="Idioma"
          subtitle={getLanguageName(settings.language)}
          onPress={handleLanguageChange}
        />
        
        <SettingItem
          icon="palette"
          title="Tema"
          subtitle={getThemeName(settings.theme)}
          onPress={handleThemeChange}
        />
        
        <SettingItem
          icon="notifications"
          title="Notificaciones"
          subtitle="Recibir notificaciones de la app"
          rightElement={
            <Switch
              value={settings.notifications}
              onValueChange={() => toggleSetting('notifications')}
              trackColor={{ false: '#f0f0f0', true: '#667eea' }}
              thumbColor={settings.notifications ? '#ffffff' : '#f4f3f4'}
            />
          }
        />
        
        <SettingItem
          icon="sync"
          title="Sincronización Automática"
          subtitle="Sincronizar datos automáticamente"
          rightElement={
            <Switch
              value={settings.autoSync}
              onValueChange={() => toggleSetting('autoSync')}
              trackColor={{ false: '#f0f0f0', true: '#667eea' }}
              thumbColor={settings.autoSync ? '#ffffff' : '#f4f3f4'}
            />
          }
        />
      </View>

      {/* Data Management */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Gestión de Datos</Text>
        
        <SettingItem
          icon="file-download"
          title="Exportar Datos"
          subtitle="Descargar una copia de tus datos"
          onPress={handleExportData}
          color="#4CAF50"
        />
        
        <SettingItem
          icon="delete-forever"
          title="Limpiar Datos"
          subtitle="Eliminar todos los datos de la app"
          onPress={handleClearData}
          color="#f44336"
        />
      </View>

      {/* Support */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Soporte</Text>
        
        <SettingItem
          icon="help"
          title="Ayuda"
          subtitle="Preguntas frecuentes y guías"
          onPress={() => Alert.alert('Ayuda', 'Función de ayuda en desarrollo')}
          color="#2196F3"
        />
        
        <SettingItem
          icon="contact-support"
          title="Contactar Soporte"
          subtitle="Obtener ayuda del equipo de soporte"
          onPress={handleContactSupport}
          color="#FF9800"
        />
        
        <SettingItem
          icon="info"
          title="Acerca de"
          subtitle="Información de la aplicación"
          onPress={() => Alert.alert('Acerca de', 'FLORA v1.0.0\nSistema de Cifrado Híbrido Post-Cuántico\n\nDesarrollado con ❤️ para la privacidad digital')}
          color="#9C27B0"
        />
      </View>

      {/* Legal */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Legal</Text>
        
        <SettingItem
          icon="privacy-tip"
          title="Política de Privacidad"
          subtitle="Cómo protegemos tus datos"
          onPress={() => Alert.alert('Privacidad', 'Política de privacidad en desarrollo')}
          color="#607D8B"
        />
        
        <SettingItem
          icon="gavel"
          title="Términos de Servicio"
          subtitle="Términos y condiciones de uso"
          onPress={() => Alert.alert('Términos', 'Términos de servicio en desarrollo')}
          color="#607D8B"
        />
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>
          © 2024 FLORA. Todos los derechos reservados.
        </Text>
        <Text style={styles.footerText}>
          Hecho con ❤️ para la privacidad digital
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
  appInfoContainer: {
    alignItems: 'center',
    padding: 30,
    backgroundColor: '#ffffff',
    marginBottom: 20,
  },
  appIcon: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#667eea',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 15,
  },
  appIconText: {
    fontSize: 40,
  },
  appName: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  appVersion: {
    fontSize: 16,
    color: '#666',
    marginBottom: 10,
  },
  appDescription: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
  },
  section: {
    backgroundColor: '#ffffff',
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    padding: 20,
    paddingBottom: 10,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 15,
  },
  settingInfo: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
    marginBottom: 2,
  },
  settingSubtitle: {
    fontSize: 14,
    color: '#666',
  },
  footer: {
    alignItems: 'center',
    padding: 30,
    paddingBottom: 50,
  },
  footerText: {
    fontSize: 12,
    color: '#999',
    textAlign: 'center',
    marginBottom: 5,
  },
});

export default SettingsScreen;

