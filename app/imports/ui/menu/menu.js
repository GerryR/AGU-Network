import { Programs } from '../../api/programs.js'

import './menu.css'
import './menu.html'

Template.menu.onCreated(function() {
    Meteor.subscribe('programs')
})


Template.menu.helpers({
    // Return a sorted list of all the programs in the database
    programs() {
        return Programs.find({}, {"sort": {"title": 1}})
    }
})

Template.menu.events({
    // Go to the graph-explorer using the clicked program id
    'click .program-item'(event) {
        event.preventDefault()
        const programId = event.currentTarget.name
        if (programId) {
            Router.go('/'+programId)
        }
    }
})
