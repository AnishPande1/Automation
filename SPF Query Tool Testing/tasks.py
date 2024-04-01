from robocorp.tasks import task
from SPF import SPFTool

@task
def main():
    call=SPFTool()
    call.open_browser()
    call.read_excel_and_fill_form()
    call.close()

if __name__=="__main__":
    main()

