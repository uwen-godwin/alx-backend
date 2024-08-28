import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, redis.print);
};

const displaySchoolValue = (schoolName) => {
  client.get(schoolName, (err, reply) => {
    if (err) {
      console.log(`Error: ${err.message}`);
    } else {
      console.log(reply);
    }
  });
};

// First, set a value, then display it
setNewSchool('Holberton', 'School');  // Set a value for 'Holberton'
displaySchoolValue('Holberton');      // Now display the value for 'Holberton'
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
