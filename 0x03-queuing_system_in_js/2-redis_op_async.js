import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, redis.print); // Use redis.print for the first set only
};

const displaySchoolValue = async (schoolName) => {
  const getAsync = promisify(client.get).bind(client);
  try {
    const reply = await getAsync(schoolName);
    console.log(reply);
  } catch (err) {
    console.log(`Error: ${err.message}`);
  }
};

// Set a value for 'Holberton' and then display it
setNewSchool('Holberton', 'School');   
displaySchoolValue('Holberton');        

// Set a value for 'HolbertonSanFrancisco' and then display it without "Reply: OK"
client.set('HolbertonSanFrancisco', '100'); 
displaySchoolValue('HolbertonSanFrancisco'); 
