

import svg
from textwrap import dedent    
        


class OSMsvgFile:
    """
    OSMsvgFile is a class for creating and manipulating SVG files. It provides methods for opening a new SVG file, adding SVG elements, closing the file, and writing it to a file or returning it as a string.

    Core functionalities:
    - open: Initializes the SVG file with specified dimensions and styles.
    - addsvg: Adds an SVG element to the file.
    - close: Finalizes the SVG file and returns it.
    - writeToFile: Writes the SVG file to a specified file.
    - getSVG: Returns the SVG file object.
    - getSVGString: Returns the SVG file as a string.
    - clear: Resets the SVG file to its initial state.

    
    """

    def __init__(self):
        """
        Initialize the svg object.

        This method initializes the svg object by calling the superclass's
        initializer and init internal state.
        """
        super().__init__()

        self.clear()
        

    def open (self, 
              svgstyle="""
                        
                        .small { font: 10px sans-serif; fill:black}
                        svg {background-color: white;}
                        .smallevidence { font: 10px sans-serif; fill:red}
                        .heavy { font: bold 30px sans-serif; }
                        .heavyevidence { font: bold 30px sans-serif; fill:red}
                     
                        .title { font: italic 40px sans-serif; fill:red; }
                        
                    """,
              widthmm=1000, 
              heightmm=1000):
        
        """
        Initialize the SVG file with specified style and dimensions.

        Parameters:
        svgstyle (str): The CSS style to be applied to the SVG file.
        widthmm (int): The width of the SVG file in millimeters.
        heightmm (int): The height of the SVG file in millimeters.
        """
        
        # Initialize the list of elements
        self.elements: list[svg.Element] = []
        # Set the width and height of the SVG file
        self.width = widthmm
        self.height = heightmm
        # Add the style to the list of elements
        self.elements.append (
            svg.Style(
                    text=dedent(svgstyle)
            )
        )
    
    def addsvg (self, element: svg.Element):
        """
        Add an element to the svg file.

        Args:
            element (svg.Element): The element to be added to svg file.
        """
        
        self.elements.append(element)
           

    def close (self):
        """
        Finalize the SVG file and return it. AFter calling this method the svg object is locked and wont 
        accept any more changes.

        Returns:
            svg.SVG: The py.SVG object representing the created SVG file.
        """
        # Create the SVG file with the specified width, height and elements
        
        self.fig = svg.SVG(
                viewBox=svg.ViewBoxSpec(0, 0, self.width, self.height),
                width=svg.mm(self.width),
                height=svg.mm(self.height),
                
                elements=self.elements
                )
        return self.fig
    
    def getSVG (self):
        """
        Return the SVG file as py.svg object.

        Returns:
            svg.SVG: The SVG file.
        """
        return self.fig
    
    def getSVGString (self):
        """
        Return the SVG file as a string.

        Returns:
            str: The SVG file as a string.
        """
        if self.fig:
            return str(self.fig)
        else:
            return ""
    
    def writeToFile (self, fname):
        """
        Write the SVG file to a file on disk.

        Parameters:
        fname (str): The name of the file to write to.
        """
        # Write the SVG file to a file
        if self.fig:
            with open(fname, 'w') as f:
                f.write(str(self.fig))

    def clear (self):
        """
        Clear the internal object state.
        """
        # Clear the list of elements and set the width and height to 0
        self.elements: list[svg.Element] = []
        self.fig = None
        self.width = 0
        self.height = 0



def test_OSMsvgFile():
    # Test case 1: Create an SVG file with default dimensions and styles
    svgfile1 = OSMsvgFile()
    svgfile1.open()
    svgfile1.close()
    print (svgfile1.getSVGString())
    assert svgfile1.getSVGString().startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox=')

    # Test case 2: Create an SVG file with custom dimensions and styles
    svgfile2 = OSMsvgFile()
    svgfile2.open(widthmm=500, heightmm=500, svgstyle=".small { font: 10px sans-serif; }")
    svgfile2.close()
    assert svgfile2.getSVGString().startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox=')
    assert "width=\"500mm\"" in svgfile2.getSVGString()

    # Test case 3: Add an SVG element to the file
    svgfile3 = OSMsvgFile()
    svgfile3.open()
    svgfile3.addsvg(svg.Circle(cx=50, cy=50, r=40, fill="red"))
    svgfile3.close()
    assert "circle" in svgfile3.getSVGString()

    # Test case 4: Close the SVG file and return it
    svgfile4 = OSMsvgFile()
    svgfile4.open()
    svgfile4.close()
    assert svgfile4.getSVGString().startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox=')

    # Test case 5: Write the SVG file to a file on disk
    svgfile5 = OSMsvgFile()
    svgfile5.open()
    svgfile5.addsvg(svg.Circle(cx=150, cy=150, r=40, fill="blue"))
    svgfile5.addsvg(svg.Circle(cx=400, cy=400, r=300, fill="#00ff0040"))
    svgfile5.addsvg(svg.Text(x=10, y=50, class_=["title"], text="Hello world !"))
    
    svgfile5.close()
    print(svgfile5.getSVGString())
    svgfile5.writeToFile("svgtest.svg")
    with open("svgtest.svg", 'r') as f:
        assert f.read().startswith('<svg xmlns="http://www.w3.org/2000/svg" viewBox=')

    
    # Test case 7: Clear the internal object state
    svgfile7 = OSMsvgFile()
    svgfile7.open()
    svgfile7.close()
    svgfile7.clear()
    assert svgfile7.getSVGString() == ''

    print("All test cases pass")

if __name__ == '__main__':
    test_OSMsvgFile()

