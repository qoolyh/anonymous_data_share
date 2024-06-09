class GUIModel:
    """
    record backend in graphical form, including screens and edges
    """

    def __init__(self, screens, edges):
        """
        :param screens: dictionary type
        :param edges: list type
        """

        self.screens = screens
        self.edges = edges