import { Template } from 'meteor/templating'

import { Abstracts } from '../api/abstracts.js'
import { Sessions } from '../api/sessions.js'

import './graph.css'
import './graph.html'

Template.graph.onCreated(function() {
    Session.set('currentAbstract', null)
})


Template.graph.onRendered(function() {

    const programId = Router.current().params.programId

    Meteor.subscribe('abstracts.program', Number(programId))

    const selectedColor = '#FF0000'
    const neighborColor = '#006400'

    // NOTE: update the directory according to the year
    const graphFileName = "2017/graph-" + programId + ".gexf"

    const graphInstance = this

    // Custom node renderer (only works on hover)
    // Credits to http://yomguithereal.github.io/articles/node-border-renderer/
    sigma.canvas.nodes.border = function(node, context, settings) {
        var prefix = settings('prefix') || '';

        context.fillStyle = node.color || settings('defaultNodeColor');
        context.beginPath();
        context.arc(
            node[prefix + 'x'],
            node[prefix + 'y'],
            node[prefix + 'size'],
            0,
            Math.PI * 2,
            true
        );

        context.closePath();
        context.fill();

        // Adding a border
        context.lineWidth = node.borderWidth || 2;
        context.strokeStyle = node.borderColor || selectedColor;
        context.stroke();
    };

    sigma.parsers.gexf(
        graphFileName, {
            container: 'graph-container',
            settings: {
                defaultEdgeColor: '#808080',
                edgeColor: 'default',
                defaultNodeColor: '#364d66',
                borderSize: 3,
                minNodeSize: 1,
                maxNodeSize: 1.5,
                minEdgeSize: 0.1,
                maxEdgeSize: 0.5,
                zoomMin: 0.02,
                zoomMax: 2
            }
        },
        function(s) {
            //console.log('GRAPH..')

            // Handle click on graph node
            s.bind('clickNode', function(event) {

                const id = event.data.node.id

                a = Abstracts.findOne({
                    abstractId: Number(id)
                })

                if (a != null) {
                    oldAbstract = Session.get('currentAbstract')
                    oldId = null
                    if (oldAbstract != null) {
                        oldId = oldAbstract.abstractId
                    }
                    Session.set('currentAbstract', $.extend(a, {
                        oldId: oldId
                    }))
                } else {
                    console.log("Abstract not found")
                }
            })

            // When stage is clicked, unselect current abstract
            s.bind('clickStage', function(event) {
                if (event.data.captor.isDragging == false)
                    Session.set("currentAbstract", null)
            })

            // Add two arrays to each node to limit computation:
            // 1) array containing all the edges of the node
            // 2) array containing all the neighbors
            s.graph.nodes().forEach(function(n) {
                n.allEdges = []
                n.neighbors = []
                n.type = 'border'
            });

            // Build the arrays for each node
            s.graph.edges().forEach(function(e) {
                s_node = s.graph.nodes(e.source)
                t_node = s.graph.nodes(e.target)

                s_node.allEdges.push(e)
                s_node.neighbors.push(t_node)

                t_node.allEdges.push(e)
                t_node.neighbors.push(s_node)
            })

            // This function will run every time "currentAbstract" changes
            graphInstance.autorun(function() {
                const abstract = Session.get("currentAbstract");
                if (abstract != null) {

                    // Clean old node and neighbors
                    const oldNodeId = abstract.oldId
                    if (oldNodeId != null) {
                        n = s.graph.nodes(oldNodeId)
                        if (n) {
                            n.color = null

                            n.allEdges.forEach(function(e) {
                                e.color = null
                                e.size = null
                            })

                            n.neighbors.forEach(function(c) {
                                c.color = null
                            })
                        }
                    }

                    // Update new node and neighbors
                    const nodeId = abstract.abstractId
                    n = s.graph.nodes(nodeId)

                    if (n) {
                        n.color = selectedColor

                        n.allEdges.forEach(function(e) {
                            e.color = neighborColor
                            e.size = 16
                        })

                        n.neighbors.forEach(function(c) {
                            c.color = neighborColor
                        })

                        sigma.misc.animation.camera(
                            s.camera, {
                                x: n[s.camera.readPrefix + 'x'],
                                y: n[s.camera.readPrefix + 'y'],
                                ratio: Math.min(s.camera.ratio, 0.1)
                            }, {
                                duration: 1000
                            }
                        )
                    }
                } else {
                    // If "currentAbstract" is null, clean everything
                    s.graph.nodes().forEach(function(n) {
                        n.color = null
                    });

                    s.graph.edges().forEach(function(e) {
                        e.color = null
                        e.size = null
                    })
                }

                s.refresh()
            });

            s.refresh()

            console.log('GRAPH CREATED!')
        })

})
