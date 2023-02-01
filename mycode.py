import numpy as np
import collections
from datetime import datetime
from dateutil import parser
import argparse
import csv




class transaction_points(object):
    """docstring for transaction_points"""
    def __init__(self, config):
        super(transaction_points, self).__init__()
        self.datafile = config.data_path
        self.accounts = collections.defaultdict()
        self.points = config.rp
        self.transactions = collections.deque()
        self.total_points = 0
        self.status_code = 0
        self.alldata = []
        self.points_spent = []
        self.output_saving = config.output_path
    def load_data(self):
        ### load all transaction data ###
        self.data = np.genfromtxt(self.datafile,
                 delimiter=",", dtype=str,skip_header=1)

        # print(f'data:{self.data}')
        for item in self.data:

            payer = (str(item[0])).replace('"','')
            point = int(item[1])

            time = (str(item[2])).replace('"','')
            date = datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
            self.alldata.append([payer,point,date])
        self.alldata.sort(key=lambda x:x[2])
        # print(f'all data:{self.alldata}')
    
    def add_points(self):
        '''
            1. Combine duplicated users' transaction info
            2. Update the date
            3. Sort the updated info

            When the points are positive, simply append the transaction to the queue
            When the points are negative, there are three conditions
            - when the payer already exists and deducting the incoming transactional points results in negative points value
            - when the payer already exists and deducting the incoming transactional points result in positive points value
            - when the first transactional points value is negative
        '''
        for item in self.alldata:

            payer = str(item[0])
            point = int(item[1])
            date = item[2]

            if point > 0:
                self.total_points += point
                self.transactions.appendleft([payer,point,date])
                if payer not in self.accounts:
                    self.accounts[payer] = point
                else:
                    self.accounts[payer] += point

            elif point < 0:
                if payer in self.accounts and (self.accounts[payer] - point) < 0:
                    self.status_code = 400
                    return ("Invalid transaction record:",int(self.status_code))
                
                elif payer in self.accounts and (self.accounts[payer] - point) > 0:
                    self.accounts[payer]+=point 
                    self.total_points += point
                    # self.points += abs(point)
                    for i in range(len(self.transactions)-1,-1,-1):
                        if self.transactions[i][0] == payer:
                            remaining = self.transactions[i][1] + point
                            if remaining <= 0:
                                del self.transactions[i]
                                point = remaining
                            else:
                                self.transactions[i][1] = remaining
                                break
                else:
                    self.status_code = 400
                    return ("Invalid transaction record",int(self.status_code))

        return("Points Added Successfully!",int(self.status_code))



    def redeem_points(self):
        # print(f'points deducting:{self.points}')
        # print(f'all transactions:{self.transactions}')
        if self.total_points < self.points:
            self.status_code = 400
            return("Insufficient points value !!",int(self.status_code))
        else:
            points_list = []
            while self.points > 0:

                transaction = self.transactions.pop()
                # print(f'points remaining:{self.points}')
                self.points -= transaction[1]
                # print('deducting:',transaction[1])
                # print(f'points deducting:{self.points}')
                if self.points < 0:
                    points_deducted = transaction[1] + self.points
                    transaction[1] = points_deducted
                    self.transactions.append(transaction)
                else:
                    points_deducted = transaction[1]
                transaction[1] = points_deducted
                transaction[2] = 'now'
                points_list.append(transaction)
                self.accounts[transaction[0]] -= points_deducted
                self.total_points -= points_deducted
        # print(f'points_list:{points_list}')
        # print(f'points remaining:{self.points}')
        for val in points_list:
            val[1] = -val[1]
            self.points_spent.append(val)
        
        
        with open(self.output_saving, 'w', encoding='UTF8', newline='') as f:
            ### saving spent info ###
            writer = csv.writer(f)
            writer.writerow(['Account spent Info'])
            for item in self.points_spent:
                writer.writerow(item[:2])
            writer.writerow('\n')
            ### saving balance info ###
            writer.writerow(['Account balance Info'])
            for payer in self.accounts:
                tmp = [payer,self.accounts[payer]]
                writer.writerow(tmp)
        f.close()
        print('>>> Saving is done <<<')





    def main(self):

        self.load_data()
        self.add_points()
        self.redeem_points()
        # print(f'q:{self.transactions}')
        print(f'accounts:{self.accounts}')
        # print(f'points info:{self.total_points}')
        print(f'points_spent info:{self.points_spent}')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "fetch points redeem")
    # Debug mode #
    parser.add_argument('--data_path',        type = str, default = 'transactions.csv',
                        help = 'The path of the data stored.')

    parser.add_argument('--rp',               type = int, default = 5000,
                        help = 'The total points need to redeem.')
    
    parser.add_argument('--output_path',        type = str, default = 'output.csv',
                        help = 'The path of the output.')


    config = parser.parse_args()
    tp = transaction_points(config)
    tp.main()
    


