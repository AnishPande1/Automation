from robocorp.tasks import tasks
from config import*
from Locator import locator

@tasks
def main():
    """Main function to call all classes and run it"""
    cf=locator()
    cf.open_url()
    cf.sort_data()
    cf.close_url()

if __name__=="__main__":
    main()

