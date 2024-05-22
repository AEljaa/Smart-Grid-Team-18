import { StyleSheet, Text, View, FlatList, TouchableOpacity } from 'react-native';
import { Link } from 'expo-router';
import { useEffect, useState } from 'react';
import NavBar from '../components/NavBar';

export default function Energy() {
  const [data, setData] = useState({});
  const fetchData = async () => {
    try {
      const response = await fetch('https://your-webserver-endpoint.com/data'); //Get the data from the server
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

//   const handleImport = async () => {
//     try {
//       await fetch('https://your-webserver-endpoint.com/import', { //Our own webserver that has our database
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ action: 'import' }), //http request to the server saying to import energy
//       });
//       alert('Import request sent!');
//     } catch (error) {
//       console.error(error);
//     }
//   };

//   const handleExport = async () => {
//     try {
//       await fetch('https://your-webserver-endpoint.com/export', { //Our own webserver that has our database
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ action: 'export' }), //http request to the server saying to export energy
//       });
//       alert('Export request sent!');
//     } catch (error) {
//       console.error(error);
//     }
//   };

  return (
    <View style={styles.container}>
      <NavBar/>
      <Text style={styles.title}>Energy Trading</Text>
      <View style={styles.textBox}>
      <Text style={styles.buttonText}>Import Cost</Text>
        <Text style={styles.textValue}>{2}</Text>
        <TouchableOpacity style={styles.button} onPress={() => console.log("Import")}> 
        <Text style={styles.buttonText}>Import</Text>
        </TouchableOpacity>
      </View> 
      <View style={styles.textBox}>
      <Text style={styles.buttonText}>Export Cost</Text>
        <Text style={styles.textValue}>{3}</Text>
        <TouchableOpacity style={styles.button} onPress={() => console.log("Export")}>
            <Text style={styles.buttonText}>Export</Text>
        </TouchableOpacity>
      </View>
      <Link href="/" style={styles.link}>Go to Home</Link>
    </View>
  );
}

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#150044', // Dark background color
      alignItems: 'center',
      justifyContent: 'center',
      paddingtop: 80,
      },
      link: {
        color: 'blue',
        marginTop: 20,
      },
      title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 40,
        color: 'white',
        textAlign: 'center', // Center text horizontally
      },
      textBox: {
        marginBottom: 20,
        alignItems: 'center',
      },
      textLabel: {
        color: '#e26a00',
        fontSize: 18,
        marginBottom: 5,
        textAlign: 'center', // Center text horizontally
      },
      textValue: {
        color: '#e26a00',
        fontSize: 16,
        marginBottom: 10,
        textAlign: 'center', // Center text horizontally
      },
      button: {
        backgroundColor: '#007bff',
        padding: 15,
        borderRadius: 10,
        marginTop: 10,
        width: 200, // Adjust the width as needed
        alignItems: 'center',
      },
      buttonText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
      }
});
