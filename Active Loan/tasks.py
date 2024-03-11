from robocorp.tasks import tasks
from ActiveLoan import Loan

@tasks
def main():
    """Main function to call all classes and run it"""
    cf = Loan()
    cf.execute()

if __name__ == "__main__":
    main()
