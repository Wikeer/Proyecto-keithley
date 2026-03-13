from visautils import resource_list
from gui import window_creation

def main():
    recursos = resource_list()
    window = window_creation(recursos)
    window.mainloop()

if __name__ == "__main__":
    main()
    
