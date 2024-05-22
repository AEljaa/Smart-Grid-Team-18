import { StyleSheet, Text, View, FlatList,ScrollView } from 'react-native';
import { Link } from 'expo-router';
import NavBar from '../components/NavBar';
import { useEffect, useState } from 'react';

export default function Home() {
  // Declaring state variable 'data' with initial value as an empty object
//   const [data, setData] = useState({});
  // Function to fetch data from the third party web server and update the state variable 'data'
//   const fetchData = async () => {
//     try {
//       const response = await fetch('https://your-webserver-endpoint.com/data');
//       const result = await response.json();
//       setData(result);
//     } catch (error) {
//       console.error(error);
//     }
//   };
//   // useEffect to fetch data on component mount and set an interval to update it every 5 seconds
//   useEffect(() => {
//     fetchData();
//     const interval = setInterval(fetchData, 5000);
//     return () => clearInterval(interval);
//   }, []);


  return (
    <View style={styles.container}>
      <NavBar />
      <View style={styles.content}>
        <Text style={styles.title}>Current Energy Information</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.scrollContent}>
        <View style={styles.textBox}>
          <Text style={styles.textLabel}>Sun Irradiance</Text>
          <Text style={styles.textValue}>{73}{"W/m2"}</Text>
        </View>
        <View style={styles.textBox}>
          <Text style={styles.textLabel}>Instantaneous Demand</Text>
          <Text style={styles.textValue}>{45}{"W"}</Text>
        </View>        
        <View style={styles.textBox}>
          <Text style={styles.textLabel}>Price Per Watt</Text>
          <Text style={styles.textValue}>{0.37}</Text>
        </View>        
        <View style={styles.textBox}>
          <Text style={styles.textLabel}>Generated Solar Power</Text>
          <Text style={styles.textValue}>{100}{"W"}</Text>
        </View>        
        <View style={styles.textBox}>
          <Text style={styles.textLabel}>Stored Power</Text>
          <Text style={styles.textValue}>{23}{"W"}</Text>
        </View>      
        </ScrollView>
        <Link href="/energy" style={styles.link}>Go to Energy Trading</Link>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#150044', //  background color
    paddingTop: 60, // Adjust padding to accommodate navbar height
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 40, // Additional padding to ensure content is not hidden behind the navbar
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 40,
    color: '#F063FE',
    textAlign: 'center',
    textShadowOffset: { width: 0, height: 0 },
  },
  textBox: {
    marginHorizontal: 10, // Add margin horizontally between text boxes
    backgroundColor: '#0D002D',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
    shadowColor: '#150345',
    shadowOpacity: 0.8,
    shadowRadius: 10,
    height: 200,
    
  },
  textLabel: {
    color: 'white',
    fontSize: 20,
    marginBottom: 10,
    textAlign: 'center',
    fontWeight: 'bold',
  },
  textValue: {
    color: '#ffffff',
    fontSize: 18,
    textAlign: 'center',
  },
  link: {
    color: '#00e5ff',
    marginTop: 20,
    fontSize: 18,
    padding: 10,
  },
  scrollContent: {
    alignItems: 'center', // Center content horizontally within the ScrollView
  }
});
