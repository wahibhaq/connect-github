from fetchdata import GithubFetch
import getpass
import json

print "\n**Loggin In**\n"

#username = raw_input("Enter github username : ") #wahibhaq
#password = getpass.getpass() 

username = "wahibhaq"
password = "githu3|P@kiblue1@#"

x = GithubFetch(username, password)

'''Profile'''
print "\n**Profile**\n"

print x.fetch_profile_data()


'''Organization'''
print "\n**Organization**\n"

for i in range(1, len(x.fetch_all_orgs_data()) + 1):
    print x.fetch_all_orgs_data().get(i)
    print "\n"

'''Repos'''
print "\n**Repository**\n"

print "**All Repository**\n"

all_repos_list = {}
all_repos_list = x.fetch_all_repos_data()
for i in range(1,len(all_repos_list) + 1) :
    print all_repos_list.get(i)
    print "\n"


print "**One Specific Repository**\n"

print x.fetch_repo_detail('android-opencv-lanedetection')









'''MAIN CODE'''


'''
1) storing github profile
2) storing github Organization
3) storing github profile - Organization (many-many)
4) storing github repos
    5) storing portfolio project 
    6) storing portfolio project - profile (many-many)
'''
