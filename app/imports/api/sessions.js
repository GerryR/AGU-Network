import {Mongo} from 'meteor/mongo';

// Mongo collection containing all the sessions
export const Sessions = new Mongo.Collection('sessions')

if (Meteor.isServer) {
    // This code only runs on the server
    Meteor.publish('sessions', function(programId) {
        return Sessions.find({programId: programId})
    })
}
