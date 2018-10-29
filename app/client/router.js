import '/imports/ui/menu/menu.js'
import '/imports/ui/graph-explorer.js'

import { Programs } from '/imports/api/programs.js'

// Go to the landing page
Router.route('/', {
    name: 'menu.show',
    template: 'menu'
})

// Go to the graph explorer
Router.route('/:programId', {
    name: 'graphExplorer.show',
    template: 'graphExplorer'
})
