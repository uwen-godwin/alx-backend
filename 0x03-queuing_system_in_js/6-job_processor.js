import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Define the function to send notification
function sendNotification(phoneNumber, message, job, done) {
  // Track job progress
  job.progress(0, 100);

  // Blacklist numbers
  const blacklisted = ['4153518780', '4153518781'];
  if (blacklisted.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // Simulate sending notification
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  
  // Update job progress and complete it
  job.progress(50, 100);
  done();
}

// Process jobs
queue.process('push_notification_code', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
