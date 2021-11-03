from datetime import datetime
from jobcoin import doler
from jobcoin import jobcoin
import click
import sys
import threading
import uuid

doler = doler.Doler()

def background():
    doler_thread = threading.Thread(target=doler.start, args=())
    doler_thread.daemon = True
    doler_thread.start()

@click.command()
def main(args=None):
    client = jobcoin.Client()
    
    print('Welcome to the Jobcoin mixer!\n')
    
    while True:
        addresses = click.prompt(
            'Please enter a comma-separated list of new, unused Jobcoin '
            'addresses where your mixed Jobcoins will be sent.',
            prompt_suffix='\n[blank to quit] > ',
            default='',
            show_default=False)
        
        addresses = addresses.strip()
        if addresses == '':
            if click.confirm('Are you sure you want to abort?', abort=True):
                sys.exit(0)
            continue
            
        addresses = addresses.split()
        
        deposit_address = uuid.uuid4().hex
        
        click.echo(
            '\nYou may now send Jobcoins to address {deposit_address}. They '
            'will be mixed and sent to your destination addresses.\n'
              .format(deposit_address=deposit_address))
        
        timestamp = datetime.now().timestamp()
        client.put(deposit_address, { "timestamp": timestamp, "addresses": addresses })

if __name__ == '__main__':
    background()
    sys.exit(main())