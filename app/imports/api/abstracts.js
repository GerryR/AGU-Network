import {Mongo} from 'meteor/mongo';

// Mongo collection containing all the abstracts
export const Abstracts = new Mongo.Collection('abstracts')

import { Programs } from './programs.js'
import { Sessions } from './sessions.js'

if (Meteor.isServer) {
  // This code only runs on the server
  Meteor.publish('abstracts.program', function(programId) {
    sessions = Sessions.find({programId: programId})

    var sessionIds = []
    sessions.forEach(function (row) {
        sessionIds.push(row.sessionId)
    })

    return Abstracts.find({sessionId: {"$in": sessionIds}});
  });
}
