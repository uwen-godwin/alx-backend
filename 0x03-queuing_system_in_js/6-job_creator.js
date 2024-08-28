import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Create job data
const jobData = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account'
};

// Create a job
const job = queue.create('push_notification_code', jobData).save((err) => {
  if (err) {
    console.log('Notification job failed to create');
  } else {
    console.log(`Notification job created: ${job.id}`);
  }
});

// Handle job completion
job.on('complete', () => {
  console.log('Notification job completed');
});

// Handle job failure
job.on('failed', (err) => {
  console.log(`Notification job failed: ${err}`);
});
