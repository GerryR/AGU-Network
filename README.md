# AGU NETWORK

## Demo

Try the [AGU Network webapp](https://agunetwork.herokuapp.com)!

## Description

![AGU Network on Desktop](/screenshots/agunetwork-screen1.png?raw=true "AGU Network on Desktop")

The goal of this project is to develop a web-based interactive network showing how the 
different works presented during the AGU are related to each other. 
The relation between a pair of abstracts is computed using a semantic similarity measure based 
on the information provided by the AGU API, providing a weight for each link. The length of a 
link connecting two abstracts is inversely proportional to its weight, allowing the formation
of clusters containing abstracts strictly related to each other.

There is a network for each conference program and the 
AGU participants can take advantage from this website by quickly spotting abstracts 
related to what they are presenting. It is possible to understand how 
the different sessions or clusters are related to each other and how such relations 
are evolving during the years. The process and code to build the network can be 
easily re-used for other conferences.

## Mobile

The web application can be used on mobile phones. The sidebar is visible only in landscape mode.
When using the portrait mode, a warning message appears on the bottom.

![AGU Network on Mobile](/screenshots/agunetwork-mobile-preview.png?raw=true "AGU Network on Mobile")

## Folder Structure

The repository contains two folders:

1. `pyagu`: python scripts to download data from the API, analyze it and build the graph
2. `app`: web-app developed using the `meteor.js` framework

More information can be found into each folder and through the comments in the code.

## Author
Calogero B. Rizzo, University of Southern California, calogerr@usc.edu.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [Meteor.js](https://www.meteor.com/): reactive framework to build web application
- [Sigma.js](http://sigmajs.org/): javascript library for interactive graphs
- [NLTK](http://www.nltk.org/): natural language toolkit for Python
- [Gephi](https://gephi.org/): graph visualization software

