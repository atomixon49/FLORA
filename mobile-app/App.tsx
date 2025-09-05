import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import EncryptScreen from './src/screens/EncryptScreen';
import DecryptScreen from './src/screens/DecryptScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import FilesScreen from './src/screens/FilesScreen';
import SecurityScreen from './src/screens/SecurityScreen';

// Types
export type RootStackParamList = {
  Main: undefined;
  Encrypt: undefined;
  Decrypt: undefined;
  Files: undefined;
  Security: undefined;
  Settings: undefined;
};

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator<RootStackParamList>();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: string;

          switch (route.name) {
            case 'Home':
              iconName = 'home';
              break;
            case 'Encrypt':
              iconName = 'lock';
              break;
            case 'Decrypt':
              iconName = 'lock-open';
              break;
            case 'Files':
              iconName = 'folder';
              break;
            case 'Security':
              iconName = 'security';
              break;
            case 'Settings':
              iconName = 'settings';
              break;
            default:
              iconName = 'help';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#667eea',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: {
          backgroundColor: '#ffffff',
          borderTopColor: '#e0e0e0',
          height: 60,
          paddingBottom: 8,
          paddingTop: 8,
        },
        headerStyle: {
          backgroundColor: '#667eea',
        },
        headerTintColor: '#ffffff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen} 
        options={{ 
          title: '🌸 FLORA',
          headerTitle: '🌸 FLORA - Cifrado Seguro'
        }} 
      />
      <Tab.Screen 
        name="Encrypt" 
        component={EncryptScreen} 
        options={{ 
          title: 'Cifrar',
          headerTitle: '🔐 Cifrar Datos'
        }} 
      />
      <Tab.Screen 
        name="Decrypt" 
        component={DecryptScreen} 
        options={{ 
          title: 'Desifrar',
          headerTitle: '🔓 Desifrar Datos'
        }} 
      />
      <Tab.Screen 
        name="Files" 
        component={FilesScreen} 
        options={{ 
          title: 'Archivos',
          headerTitle: '📁 Gestión de Archivos'
        }} 
      />
      <Tab.Screen 
        name="Security" 
        component={SecurityScreen} 
        options={{ 
          title: 'Seguridad',
          headerTitle: '🛡️ Centro de Seguridad'
        }} 
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen} 
        options={{ 
          title: 'Configuración',
          headerTitle: '⚙️ Configuración'
        }} 
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar barStyle="light-content" backgroundColor="#667eea" />
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Main" component={MainTabs} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
});

