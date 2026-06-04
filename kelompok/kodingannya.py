# AABDUSS SYAKUR INI YACH
# membuat logic untuk visusalisasi streamlit tentang kebutuhan sehari-hari menggunakan graf
import networkx as nx

# kelas untuk kebutuhan sehari-hari dengan graf
class KebutuhanSehariHari:
    # init untuk membuat graph kosong
    def __init__(self):
        
        self.graph = nx.Graph()

    # method untuk menambahkan kebutuhan ke dalam graph
    def tambah_kebutuhan(self, kebutuhan):
        
        if kebutuhan not in self.graph:
            self.graph.add_node(kebutuhan)
            return True
        return False

    def add_hubungan(self, kebutuhan1, kebutuhan2, bobot):
        if self.graph.has_node(kebutuhan1) and self.graph.has_node(kebutuhan2):
            self.graph.add_edge(kebutuhan1, kebutuhan2, weight=bobot)
            return True
        return False
        
    # fungsi untuk mendapatkan graph kebutuhan
    def get_kebutuhan(self):
        return self.graph
    
    # fungsi untuk mendapatkan semua kebutuhan
    def get_all_kebutuhan(self):
        return self.graph.nodes()
    
    # fungsi untuk mendapatkan semua hubungan
    def get_all_hubungan(self):
        return self.graph.edges()
    
    # fungsi untuk mendapat semua kebutuhan dengan bobot dalam graf
    def get_kebutuhan_dengan_bobot(self):
        return self.graph.edges(data=True)
    
    # fungsi untuk mendapatkan kebutuhan dengan bobot tertentu
    def get_hubungan_dengan_bobot(self):
        return self.graph.edges(data=True)
    # fungsi untuk menghapus kebutuhan dari graf
    def hapus_kebutuhan(self, kebutuhan):
        if kebutuhan in self.graph:
            self.graph.remove_node(kebutuhan)
            return True
        return False