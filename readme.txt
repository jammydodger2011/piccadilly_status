Piccadilly Line Status Checker

Case for AWS SES:

I've created a lambda funciton whcih runs on a schedule to retrieve the status of a line on the London underground. I'd like to use SES to send the status via email to my 3 flatmates if the status is not running with 'good service'. I opted for SES over SNS due to the customisability of the email body.

Q: How do you plan to build or acquire your mailing list?
A: Friends who consent to me manually adding them to the recipient list

Q: How do you plan to handle bounces and complaints?
A: By removing any email addresses that bounce or the recipient requests I remove them from recipient list. There will be so few recipients that all this can be maintained manually.

Q: How can recipients opt out of receiving email from you?
A: They can reply to the verified sender address requesting to be removed or contact me directly though any other channels. With so few recipients, I can remove their adresses manually.

Q: How did you choose the sending rate or sending quota that you specified in this request?
A: Sending rate: 5; Sending quota: 100
The solution will send a maximum of two emails per recipient per day. With 4 recipients, this will be 8. 100 was chosen as the quota so I have room to expand recipients and email frequency. Sending rate of 5 lets me send to all 4 recipients within a second, but this isn't critical.




