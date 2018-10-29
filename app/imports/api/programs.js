import {Mongo} from 'meteor/mongo';

// Mongo collection containing all the programs
export const Programs = new Mongo.Collection('programs')

if (Meteor.isServer) {
    // This code only runs on the server
    Meteor.publish('programs', function() {
        return Programs.find({})
    })
}
