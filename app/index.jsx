import { StyleSheet, Text, View, FlatList } from 'react-native';
import { Link } from 'expo-router';
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
        <Text style={styles.appName}>Power Grid App</Text>
        <View style={styles.textBox}>
          <Text style={styles.textLabel}>Sun Irradiance</Text>
          <Text style={styles.textValue}>{73}</Text>
        </View>
        <View style={styles.textBox}>
          <Text style={styles.textLabel}>Instantaneous Demand</Text>
          <Text style={styles.textValue}>{100}</Text>
        </View>
        <Link href="/energy" style={styles.link}>Go to Energy Trading</Link>
      </View>
  );
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
    resizeMode: 'cover',
    justifyContent: 'center',
  },
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  appName: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: 'black',
    textAlign: 'center', // Center text horizontally
    position: 'absolute', // Position element absolutely
    top: 40, // Adjust this value to move the title higher or lower
  },
  textBox: {
    marginBottom: 20,
  },
  textLabel: {
    color: 'black',
    fontSize: 18,
    marginBottom: 5,
    textAlign : 'center',
  },
  textValue: {
    color: 'black',
    fontSize: 16,
    textAlign: 'center',
  },
  link: {
    color: 'blue',
    marginTop: 10,
  },
});
