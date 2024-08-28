const express = require('express');
const kue = require('kue');
const redis = require('redis');
const { promisify } = require('util');

// Initialize Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Initialize Kue queue
const queue = kue.createQueue();

// Initialize Express app
const app = express();
const port = 1245;

// Initialize reservation settings
const INITIAL_SEATS = 50;
let reservationEnabled = true;

// Function to reserve a seat
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Function to get current available seats
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats;
}

// Set initial available seats
reserveSeat(INITIAL_SEATS);

// Route to get available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

// Route to process the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    try {
      const currentSeats = await getCurrentAvailableSeats();
      const newSeats = Number(currentSeats) - 1;
      if (newSeats < 0) {
        throw new Error('Not enough seats available');
      }
      await reserveSeat(newSeats);
      if (newSeats === 0) {
        reservationEnabled = false;
      }
      console.log(`Seat reservation job ${job.id} completed`);
      done();
    } catch (error) {
      console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
      done(error);
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

