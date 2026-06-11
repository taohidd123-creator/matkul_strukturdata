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

# method untuk menambahkan hubungan antara kebutuhan dengan bobot tertentu
    def add_hubungan(self, kebutuhan1, kebutuhan2, bobot):
        if self.graph.has_node(kebutuhan1) and self.graph.has_node(kebutuhan2):
            if self.graph.has_edge(kebutuhan1, kebutuhan2):
                current_weight = self.graph.edges[kebutuhan1, kebutuhan2].get('weight', 0)
                self.graph.edges[kebutuhan1, kebutuhan2]['weight'] = current_weight + bobot
            else:
                self.graph.add_edge(kebutuhan1, kebutuhan2, weight=bobot)
            return True
        return False
        
    # fungsi untuk mendapatkan graph kebutuhan
    def get_kebutuhan(self):
        return self.graph 
    
    # fungsi untuk mendapatkan semua kebutuhan dalam graf
    def get_all_kebutuhan(self):
        return self.graph.nodes()
    
    # fungsi untuk mendapatkan semua hubungan dengan bobot dalam graf
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
        if kebutuhan not in self.graph:
            return False

        tanggal_node = None
        kebutuhan_weight = 0

        for neighbor in self.graph.neighbors(kebutuhan):
            if "Tgl " in str(neighbor):
                tanggal_node = neighbor
                kebutuhan_weight = self.graph.edges[kebutuhan, neighbor].get('weight', 0)
                break

        if tanggal_node is not None and self.graph.has_edge("Dana Bulanan", tanggal_node):
            remaining_kebutuhan = [
                node for node in self.graph.neighbors(tanggal_node)
                if node != "Dana Bulanan" and node != kebutuhan
            ]

            current_weight = self.graph.edges["Dana Bulanan", tanggal_node].get('weight', 0)
            new_weight = max(0, current_weight - kebutuhan_weight)

            if not remaining_kebutuhan or new_weight == 0:
                self.graph.remove_edge("Dana Bulanan", tanggal_node)
            else:
                self.graph.edges["Dana Bulanan", tanggal_node]['weight'] = new_weight

        self.graph.remove_node(kebutuhan)

        if tanggal_node is not None and tanggal_node in self.graph and self.graph.degree[tanggal_node] == 0:
            self.graph.remove_node(tanggal_node)

        return True
