import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';
import chai from 'chai';

const { expect } = chai;
const queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
  before((done) => {
    queue.testMode.enter();
    done();
  });

  after((done) => {
    queue.testMode.exit();
    queue.testMode.clear();
    done();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('should create jobs and log their creation', (done) => {
    const jobs = [{ phoneNumber: '4153518780', message: 'Test message' }];
    createPushNotificationsJobs(jobs, queue);

    queue.testMode.jobs((err, jobs) => {
      expect(err).to.be.null;
      expect(jobs.length).to.equal(1);
      done();
    });
  });
});
