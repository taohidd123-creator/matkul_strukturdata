class Node:
    def __init__(self, data):
        self.data = data # data akan di wakilkan oleh variabel data
        self.next = None # variabel next akan menunjuk ke node selanjutnya

class linkedList:
    def __init__(self): # konstruktor untuk inisialisasi linked list
        self.head = None # variabel head akan menunjuk ke node pertama dalam linked list
    
    def add_list(self, data):
        
        new_node = Node(data) # membuat node baru dengan data yang diberikan
        new_node.next = self.head # node baru akan menunjuk ke node yang saat ini menjadi head
        self.head = new_node # head sekarang akan menunjuk ke node baru

    def display(self): # untuk menampilkan isi linked list
        temp = self.head # variabel temp akan digunakan untuk traversing linked list
        while temp: # selama temp tidak None
            print(temp.data, end=" -> ") # cetak data dari node saat ini
            temp = temp.next # pindah ke node berikutnya

    def delete_list(self, data): # untuk menghapus node
        temp = self.head
        while temp:
            if temp.data == data:
                if temp == self.head:
                    self.head = temp.next
                else:
                    temp.next = temp.next.next
                print("Data berhasil dihapus")
                break
            temp = temp.next
            print("Data tidak ditemukan")

    def search_list(self, data): # untuk mencari node
        temp = self.head
        while temp:
            if temp.data == data:
                print("data ditemukan")
                break
            temp = temp.next
        print("data tidak ditemukan")

ll = linkedList() # membuat instance dari linkedList
ll.add_list(30)
print("Cetak linkedlist")
ll.display() # menampilkan isi linked list
ll.add_list(20)
ll.add_list(10)
print("Cetak linkedlist")
ll.display()
ll.delete_list(10)
print("Cetak linkedlist")
ll.display()
ll.search_list(30)