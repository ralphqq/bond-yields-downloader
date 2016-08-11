import os
from datetime import datetime, timedelta
from time import sleep
from urlparse import urlparse

import requests
from dateutil import parser
from requests.exceptions import RequestException

FILE_URL = 'http://www.pds.com.ph/wp-content/uploads/%s/govt_sec_rates_%s.csv'
OUTPUT_DIR = 'Downloads'

MIN_DATE = datetime(2015, 1, 26)            # The earliest report on PDS site
MAX_DATE = datetime.now()

WAIT_TIME = 2                           # seconds

class BondYieldDownloader(object):
    """Defines the downloader object."""
    
    def __init__(self):
        """Initializes the downloader for action."""
        self.params = {}
        self.counts = 0
        self.failed = 0
        self.path = os.path.join(os.getcwd(), OUTPUT_DIR)
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    
    def run(self):
        """Starts and controls the downloader."""
        try:
            self._prompt_user()
            self._validate()
            
            specified_date = self.params['report date']
            print 'Starting download.'
            
            if specified_date is not None:
                self._download_file(specified_date)
            else:
                rp_date = self.params['start']
                one_day = timedelta(days=1)
                
                while rp_date <= self.params['end']:
                    if rp_date.weekday() <= 4:             # No weekends
                        self._download_file(rp_date)
                    
                    rp_date += one_day
                    sleep(WAIT_TIME)
        except Exception as e:
            print '%s\n' % e
        else:
            print 'Finished.\n'
            self._show_summary()
    
    def _prompt_user(self):
        """Asks user to specify certain parameters"""
        print '\nPlease enter the ff. Just leave blank to accept default.\n'
        self._handle_param(param='start',
                           msg='Starting date (Ex. Feb 1, 2016): ')
        self._handle_param(param='end',
                           msg='Ending date (Ex. Aug 1, 2016): ')
    
    def _handle_param(self, param, msg):
        """Handles user inputs"""
        while True:
            try:
                datestr = raw_input(msg)
                self.params[param] = self._date_from_str(
                    date_entry=param,
                    date_str=datestr
                )
            except Exception as e:
                print e
            else:
                break
    
    def _date_from_str(self, date_entry, date_str):
        """Converts user-specified date into correct datetime object."""
        dt_obj = None
        if date_str:
            dt_obj = parser.parse(date_str)
            if dt_obj < MIN_DATE or dt_obj > MAX_DATE:
                prompt = 'Please keep dates within Jan 1, 2015 up to today.'
                raise ValueError(prompt)
        
        return dt_obj
    
    def _validate(self):
        """Checks date params and infers mode accordingly."""
        self.params['report date'] = None
        if any(self.params.values()):
            s = self.params['start']
            e = self.params['end']
            cond1 = s is None
            cond2 = e is None
            
            if cond1 and not cond2:
                self.params['report date'] = e
            if not cond1 and cond2:
                self.params['report date'] = s
            if not cond1 and not cond2:
                if s == e:
                    self.params['report date'] = s
                else:
                    if s > e:
                        self.params['start'] = e
                        self.params['end'] = s
        else:
            self.params['report date'] = MAX_DATE
        
    def _download_file(self, report_date):
        """Downloads the file at the given url."""
        fdate = report_date.strftime('%Y-%m-%d')
        ddate = '/'.join(fdate.split('-')[:-1])
        link = FILE_URL % (ddate, fdate)
        name = os.path.basename(urlparse(link).path)
        
        try:
            print ' Accessing %s.' % name
            r = requests.get(link, stream=True)
            r.raise_for_status()
        except RequestException as e:
            status = r.status_code
            
            if status == 404:
                pass
            if status >= 500:
                print '  - Unable to download %s: %s\n' % (name, e)
                self.failed += 1
        else:
            print '  - Downloading %s.' % name
            fpath = os.path.join(self.path, name)
            
            with open(fpath, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            
            self.counts += 1
            print '  - Saved %s.' % name
    
    def _show_summary(self):
        """Displays the file counts and failures."""
        print 'Summary:'
        print '  Reports downloaded successfully: %d' % self.counts
        print '  Reports not downloaded: %d\n' % self.failed

if __name__ == '__main__':
    d = BondYieldDownloader()
    d.run()
