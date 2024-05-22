import React from 'react';
import { StyleSheet, View, Text } from 'react-native';
import NavBar from '../components/NavBar';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';

export default function HistoricPage() {
  // Sample data (replace this with your actual data from the JSON file)
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        data: [0.20, 0.45, 0.28, 0.80, 0.99, 0.43],
      },
    ],
  };

  return (
    <View style={styles.container}>
      <NavBar />
        <View style={styles.content}>
          <Text style={styles.title}>Price Per Watt History</Text>
          <LineChart
            data={data}
            width={Dimensions.get('window').width - 40} // Adjust the width as needed
            height={220}
            yAxisLabel="$"
            chartConfig={{
              backgroundColor: '#FFFFFF',
              backgroundGradientFrom: '#EAB4D3',
              backgroundGradientTo: '#150044',
              decimalPlaces: 2,
              color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
              labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
              style: {
                borderRadius: 16,
              },
              propsForDots: {
                r: '6',
                strokeWidth: '2',
                stroke: '#ffa726',
              },
            }}
            bezier
            style={{
              marginVertical: 8,
              borderRadius: 16,
            }}
          />
        </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#150044',
    paddingTop: 60, // Adjust padding to accommodate navbar height
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 40,
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#FFFFFF',
    textAlign: 'center',
    textShadowOffset: { width: 0, height: 0 },
  },
});
