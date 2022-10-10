import matplotlib.pyplot as plt


class SolDrawer:
    @staticmethod
    def get_cmap(n, name='hsv'):
        return plt.cm.get_cmap(name, n)

    @staticmethod
    def draw(name, sol, nodes):
        plt.clf()
        SolDrawer.drawPoints(nodes)
        SolDrawer.drawRoutes(sol)
        plt.savefig(str(name))

    @staticmethod
    def drawPoints(cust_list):
        x = []
        y = []
        for i in cust_list:
            
            x.append(i.x)
            y.append(i.y)
        plt.scatter(x, y, c="blue")
        plt.show()

    @staticmethod
    def drawPointsUsed(cust_list):
        x = []
        y = []
        for i in cust_list:
            if i.added == True:
            
                x.append(i.x)
                y.append(i.y)
        plt.scatter(x, y, c="blue")
        plt.show()


    @staticmethod
    def drawRoutes(route_list):
        cmap = SolDrawer.get_cmap(20)

        for r in range(0, len(route_list)):
            l1 = []
            l2 = []
            rt = route_list[r].route
            for i in range(0, len(rt) - 1):
                c0 = rt[i]
                c1 = rt[i + 1]
                plt.plot([c0.x, c1.x], [c0.y, c1.y],c=cmap(r))
        
       

