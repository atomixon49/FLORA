import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Alert,
  Modal,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface FileItem {
  id: string;
  name: string;
  size: number;
  encrypted: boolean;
  date: string;
}

const FilesScreen: React.FC = () => {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [selectedFile, setSelectedFile] = useState<FileItem | null>(null);
  const [modalVisible, setModalVisible] = useState(false);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      const savedFiles = await AsyncStorage.getItem('files');
      if (savedFiles) {
        setFiles(JSON.parse(savedFiles));
      }
    } catch (error) {
      console.error('Error loading files:', error);
    }
  };

  const saveFiles = async (newFiles: FileItem[]) => {
    try {
      await AsyncStorage.setItem('files', JSON.stringify(newFiles));
      setFiles(newFiles);
    } catch (error) {
      console.error('Error saving files:', error);
    }
  };

  const addSampleFile = () => {
    const newFile: FileItem = {
      id: Date.now().toString(),
      name: `documento_${files.length + 1}.txt`,
      size: Math.floor(Math.random() * 1000) + 100,
      encrypted: Math.random() > 0.5,
      date: new Date().toISOString(),
    };
    
    const newFiles = [...files, newFile];
    saveFiles(newFiles);
  };

  const toggleEncryption = (fileId: string) => {
    const updatedFiles = files.map(file =>
      file.id === fileId ? { ...file, encrypted: !file.encrypted } : file
    );
    saveFiles(updatedFiles);
  };

  const deleteFile = (fileId: string) => {
    Alert.alert(
      'Eliminar Archivo',
      '¿Estás seguro de que quieres eliminar este archivo?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Eliminar',
          style: 'destructive',
          onPress: () => {
            const updatedFiles = files.filter(file => file.id !== fileId);
            saveFiles(updatedFiles);
          },
        },
      ]
    );
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const renderFileItem = ({ item }: { item: FileItem }) => (
    <TouchableOpacity
      style={styles.fileItem}
      onPress={() => {
        setSelectedFile(item);
        setModalVisible(true);
      }}
    >
      <View style={styles.fileIcon}>
        <Icon
          name={item.encrypted ? 'lock' : 'lock-open'}
          size={24}
          color={item.encrypted ? '#4CAF50' : '#FF9800'}
        />
      </View>
      <View style={styles.fileInfo}>
        <Text style={styles.fileName}>{item.name}</Text>
        <Text style={styles.fileDetails}>
          {formatFileSize(item.size)} • {formatDate(item.date)}
        </Text>
      </View>
      <View style={styles.fileActions}>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => toggleEncryption(item.id)}
        >
          <Icon
            name={item.encrypted ? 'lock-open' : 'lock'}
            size={20}
            color="#2196F3"
          />
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => deleteFile(item.id)}
        >
          <Icon name="delete" size={20} color="#f44336" />
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  const FileModal = () => (
    <Modal
      animationType="slide"
      transparent={true}
      visible={modalVisible}
      onRequestClose={() => setModalVisible(false)}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          {selectedFile && (
            <>
              <View style={styles.modalHeader}>
                <Icon
                  name={selectedFile.encrypted ? 'lock' : 'lock-open'}
                  size={32}
                  color={selectedFile.encrypted ? '#4CAF50' : '#FF9800'}
                />
                <Text style={styles.modalTitle}>{selectedFile.name}</Text>
              </View>
              
              <View style={styles.modalInfo}>
                <View style={styles.infoRow}>
                  <Text style={styles.infoLabel}>Tamaño:</Text>
                  <Text style={styles.infoValue}>{formatFileSize(selectedFile.size)}</Text>
                </View>
                <View style={styles.infoRow}>
                  <Text style={styles.infoLabel}>Estado:</Text>
                  <Text style={[styles.infoValue, { color: selectedFile.encrypted ? '#4CAF50' : '#FF9800' }]}>
                    {selectedFile.encrypted ? 'Cifrado' : 'Sin cifrar'}
                  </Text>
                </View>
                <View style={styles.infoRow}>
                  <Text style={styles.infoLabel}>Fecha:</Text>
                  <Text style={styles.infoValue}>{formatDate(selectedFile.date)}</Text>
                </View>
              </View>
              
              <View style={styles.modalActions}>
                <TouchableOpacity
                  style={[styles.modalButton, styles.encryptButton]}
                  onPress={() => {
                    toggleEncryption(selectedFile.id);
                    setModalVisible(false);
                  }}
                >
                  <Icon
                    name={selectedFile.encrypted ? 'lock-open' : 'lock'}
                    size={20}
                    color="#ffffff"
                  />
                  <Text style={styles.modalButtonText}>
                    {selectedFile.encrypted ? 'Desifrar' : 'Cifrar'}
                  </Text>
                </TouchableOpacity>
                
                <TouchableOpacity
                  style={[styles.modalButton, styles.closeButton]}
                  onPress={() => setModalVisible(false)}
                >
                  <Text style={[styles.modalButtonText, { color: '#666' }]}>Cerrar</Text>
                </TouchableOpacity>
              </View>
            </>
          )}
        </View>
      </View>
    </Modal>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>
          {files.length} archivo{files.length !== 1 ? 's' : ''}
        </Text>
        <TouchableOpacity style={styles.addButton} onPress={addSampleFile}>
          <Icon name="add" size={24} color="#ffffff" />
        </TouchableOpacity>
      </View>

      {files.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Icon name="folder-open" size={64} color="#ccc" />
          <Text style={styles.emptyTitle}>No hay archivos</Text>
          <Text style={styles.emptySubtitle}>
            Toca el botón + para agregar archivos de prueba
          </Text>
        </View>
      ) : (
        <FlatList
          data={files}
          renderItem={renderFileItem}
          keyExtractor={(item) => item.id}
          style={styles.fileList}
        />
      )}

      <FileModal />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
  },
  addButton: {
    backgroundColor: '#667eea',
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  emptyContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#666',
    marginTop: 16,
  },
  emptySubtitle: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    marginTop: 8,
  },
  fileList: {
    flex: 1,
  },
  fileItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    padding: 15,
    marginHorizontal: 20,
    marginVertical: 5,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  fileIcon: {
    marginRight: 15,
  },
  fileInfo: {
    flex: 1,
  },
  fileName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  fileDetails: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  fileActions: {
    flexDirection: 'row',
  },
  actionButton: {
    padding: 8,
    marginLeft: 8,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 20,
    width: '80%',
    maxWidth: 400,
  },
  modalHeader: {
    alignItems: 'center',
    marginBottom: 20,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginTop: 10,
    textAlign: 'center',
  },
  modalInfo: {
    marginBottom: 20,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  infoLabel: {
    fontSize: 14,
    color: '#666',
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
  },
  modalActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  modalButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 12,
    borderRadius: 8,
    marginHorizontal: 5,
  },
  encryptButton: {
    backgroundColor: '#4CAF50',
  },
  closeButton: {
    backgroundColor: '#f0f0f0',
  },
  modalButtonText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
  },
});

export default FilesScreen;

