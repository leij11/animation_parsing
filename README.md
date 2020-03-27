# Group 02
This project aims to animate different parser algorithms with interactive method inside Jupyter Notebook.

## Dependencies:
1. Python 3
2. Jupyter Notebook
3. Python packages listed in requirements.txt. Run pip install -r requirements.txt from this directory to install them.

## Usage and Testing
Navigate to `./animation/`

Run the command `jupyter notebook`

Run each notebook and examine the output

Note: For each notebook, in order to generate a proper results, please run all the cells from start to end. \
Mixing the order of execution might result in error.

## Documentation
`fsm_animation.ipynb` \
This file contains the animation of execution of FSM. Specification of FSM machine can be found in `./fsm/`. In this notebook, we utilize ipywidgets, graphviz tool and graphviz python package. \
Firstly, user can define states, final states and transitions themselves. After that, we will pass these data into class `Graph`. Later on, object `Graph` will pass into FSM machine as a model. We can examine the FSM diagram generated from user input using `graph.draw()`. Fortunately, graphviz python package have built-in svg conversion, so we can visualize the result diagram inside the notebook. Last but not least, the notebook will generate a list of png image files in current directory, where each file represents a stage of execution. In this way, we can add an interactive slider which allows user to animate the execution of FSM.

`parse_tree_animation.ipynb` \
This file contains the animation of parse tree. In this notebook, we utilize ipywidgets, graphviz tool, graphviz python package and nltk python package. \
Firstly, user will enter the grammar and the sentence they want to derive. We will use nltk package to parse the grammar and get an abstract syntax tree. In the next step, we will replace each node inside abstract syntax tree with an object `Node(unique_id,label)`. The unique id we give to each node will help us distinguish various nodes with the same label. In addtion, we use depth first search to navigate each node inside abstract syntax tree. Once we prepared the nodes for AST, we can start generating source code for graphviz tool. We can visualize the generated code inside notebook. Later on, we will draw the graph using the generated graphviz code. Last but not least, we add an interactive slider to iterate through each derivation stage of parse tree.


`earley_parser_animation.ipynb` \
This file contains the animation of earley parser algorithm. In this notebook, the python code of algorithm is modified from Lecture notes 11. Besides that, we utilize ipywidgets package. \
Firstly, we define two class `Expr` and `Data` to store the data used for animation. After parsing the give sentence, user will be able to interact within jupyter notebook in order to show each stages of algorithm. More specifically, for each step (predict, match or complete), we will print the previous sentence and current sentence. Also, we will highlite the key character with red color for better visualization. \
In this notebook, we have two ways of animation. By default, `auto_generate` is set to `False`, which means that user need to click on the `next` button in order to proceed to next stage. If `auto_generate` is `True`, the notebook will automatically print the information of next stage for every 1 second. Please note that the example animation have 33 stages, which means that it requires 33 seconds to finish.