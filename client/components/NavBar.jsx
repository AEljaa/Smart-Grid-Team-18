import { StyleSheet, Text, View, TouchableOpacity , Image} from 'react-native';
import { useRouter } from 'expo-router';

export default function NavBar() {
  const router = useRouter();

  return (
    <View style={styles.navBar}>
        <Image
        source={require('../assets/images/logo.png')} // Adjust the path to your logo image
        style={styles.logo}
        resizeMode="contain"
      />
      <TouchableOpacity onPress={() => router.push('/')}>
        <Text style={styles.navText}>Home</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => router.push('/historic')}> 
        <Text style={styles.navText}>Data History</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => router.push('/energy')}>
        <Text style={styles.navText}>Energy Algorithm</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
    navBar: {
      width: '100%',
      flexDirection: 'row',
      justifyContent: 'flex-start', // Align items to the left
      alignItems: 'center', // Center items vertically
      backgroundColor: '#EAB4D3', // Dark background color for the navbar
      paddingVertical: 15,
      paddingHorizontal: 20,
      position: 'absolute',
      top: 0,
    },
    navText: {
      color: 'white',
      fontSize: 18,
      fontWeight: 'bold',
      marginLeft: 20, // Add some space between the logo and the buttons
    },
    logo: {
      width: 50, // Adjust the width of the logo as needed
      height: 50, // Adjust the height of the logo as needed
      marginLeft: 20, // Add some space to position the logo at the left corner
    },
  });
