import { Template } from 'meteor/templating'

import { Abstracts } from '../api/abstracts.js'
import { Sessions } from '../api/sessions.js'

import './abstract-info.js'

import './side-panel.css'
import './side-panel.html'

var randomAbstract = null

Template.sidePanel.onCreated(function() {
    Session.set("searchFilter", "")
    Session.set("currentSessions", null)

    const programId = Router.current().params.programId

    Meteor.subscribe('sessions', Number(programId), {
        onReady() {
            // Store a list of session ids for the current program
            const sessions = Sessions.find({programId: Number(programId)})

            var sessionIds = []
            sessions.forEach(function (row) {
                sessionIds.push(row.sessionId)
            })

            Session.set("currentSessions", sessionIds)
        }
    })
})

Template.sidePanel.helpers({

    // Get current abstract
    currentAbstract() {
        randomAbstract = null
        return Session.get("currentAbstract")
    },

    // Check if something is written in the search box
    filterEnabled() {
        return Session.get("searchFilter")
    },

    // Return a list of filtered abstracts
    // If search box is empty, return a random abstract from this program
    filteredAbstracts() {
        const filter = Session.get("searchFilter")
        const sessionIds = Session.get("currentSessions")

        if (sessionIds) {
            if (filter) {
                randomAbstract = null

                options = {
                    "sessionId": {"$in": sessionIds},
                    "$or": [
                        {"title": {"$regex": filter, "$options": "i"}}
                    ]
                }

                return Abstracts.find(options, {"limit": 10})
            }

            if (!randomAbstract) {
                const nAbstracts = Abstracts.find({"sessionId": {"$in": sessionIds}}).count()
                const random = Math.floor(Math.random()*nAbstracts)
                randomAbstract = Abstracts.find({"sessionId": {"$in": sessionIds}},
                    {"skip": random, "limit": 1})
            }

            return randomAbstract
        }

    },

    // If multiple authors, write "et al."
    etAll(authors) {
        if (authors.length > 1) {
            return " et al."
        }
    }
});

Template.sidePanel.events({

    // Prevent refresh page if search button is clicked
    'submit .search-abstract'(event) {
        event.preventDefault()
    },

    // Handle selection of abstract on the side panel
    'click .search-title'(event) {
        event.preventDefault()
        const text = event.target.innerText
        abstract = Abstracts.findOne({"title": text})
        Session.set("currentAbstract", abstract)
        randomAbstract = null
    },

    // On keyup, update session variable containing the filter
    'keyup #search-term'(event) {
        event.preventDefault()
        const text = event.target.value
        Session.set("searchFilter", text)
    }
})
