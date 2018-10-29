import { Meteor } from 'meteor/meteor';

import { Abstracts } from '../imports/api/abstracts.js'
import { Programs } from '../imports/api/programs.js'
import { Sessions } from '../imports/api/sessions.js'

Meteor.startup(function() {

    // Load from json file only when working locally and database is empty
    // Put the json files in the "private" folder
    if (process.env.ROOT_URL == 'http://localhost:3000/') {
        if (Abstracts.findOne() == null) {
            console.log('Load abstracts JSON file')
            // Load JSON file
            data = JSON.parse(Assets.getText('abstracts-DB.json'))
            for (i in data) {
                Abstracts.insert(data[i])
            }
        }

        if (Programs.findOne() == null) {
            console.log('Load programs JSON file')
            // Load JSON file
            data = JSON.parse(Assets.getText('programs-DB.json'))
            for (i in data) {
                Programs.insert(data[i])
            }
        }

        if (Sessions.findOne() == null) {
            console.log('Load sessions JSON file')
            // Load JSON file
            data = JSON.parse(Assets.getText('sessions-DB.json'))
            for (i in data) {
                Sessions.insert(data[i])
            }
        }
    }
});
