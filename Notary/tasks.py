from robocorp.tasks import task
from Notary import Notaries

@task
def main():
    """Main running file"""
    call=Notaries()
    call.execute()


if __name__=="__main__":
    main()