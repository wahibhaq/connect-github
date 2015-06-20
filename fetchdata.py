from github import Github, GithubException, UnknownObjectException
import github
import sys
import json


class GithubFetch:

    githubHandler = ''
    user = ''
    NoneReplacement = '' #used to replace api values which are received as None

    def __init__(self, username, password):
        #print "GithubFetch __init__ is running ..."
        global githubHandler
        global user
        global NoneReplacement
        
        #http://jacquev6.net/PyGithub/v1/utilities.html#module-github.GithubException
        #to enable showing log information. helps in troubleshooting
        #github.enable_console_debug_logging()
        
        try:
            
            githubHandler = Github(username, password)
            user = githubHandler.get_user()

            if user.login:
                print "\nLogin Status : Successful"

            NoneReplacement = ''

        except GithubException,e:
            print "\nLogin Status : Failure"
            sys.exit()


    #http://jacquev6.net/PyGithub/v1/github_objects/AuthenticatedUser.html    #no_of_repos, followers, following, organizations, languages, 
    #total_commits, username, name, avatar_url, url, location, email,
    #hireable, bio, public_repos, public_gists, created_at, update_at

    def fetch_profile_data(self):
        #print "fetch_profile_data is running.."
        profileDataList = {}

        try:

            profileDataList['name'] = user.name
            profileDataList['login'] = user.login
            profileDataList['html_url'] = user.html_url
            profileDataList['hireable'] = user.hireable
            profileDataList['location'] = user.location
            profileDataList['bio'] = user.bio
            profileDataList['created_at'] = user.created_at
            profileDataList['updated_at'] = user.updated_at
            profileDataList['company'] = user.company
            profileDataList['avatar_url'] = user.avatar_url

            #email = only primary email
            profileDataList['email'] = user.email
            
            #count of people following user
            followers_count = 0
            for follower in user.get_followers():
                followers_count += 1
                #followers_count += follower.followers #gives followers_count of my followers but not needed now
                
            profileDataList['followers_count'] = followers_count

            #count of people user is following
            following_count = 0
            for following in user.get_following():
                following_count += 1

            profileDataList['following_count'] = following_count

            #fetching count of organisation, user is associated with
            organizations_count = 0
            for organization in user.get_orgs():
                organizations_count += 1
                
            profileDataList['organizations_count'] = organizations_count


            #fetching count of public repos owned by user, are public and not forked from elsewhere
            repos_owned_count = 0
            repos_alsoforked_count = 0
            for repo in user.get_repos():
                if(not repo.private and not repo.fork):
                    repos_owned_count += 1
                if(not repo.private):
                    repos_alsoforked_count += 1

            profileDataList['repos_public_owned_count'] = repos_owned_count
            profileDataList['repos_public_alsoforked_count'] = repos_alsoforked_count

            profileDataList['repos_private_count'] = user.owned_private_repos


            for key,value in profileDataList.iteritems():
                if(key == 'repos_private_count'):
                    profileDataList[key] = 0
                elif(value == None):
                    #print "%s is null" % key
                    profileDataList[key] = NoneReplacement


        except UnknownObjectException,e:
            #this is to bypass 404 error received when field is not found
            print "Error : %s " % str(e)
 
        except GithubException,e:
            print "Error : %s " % str(e)

        finally:
            return profileDataList
    
    #number of organizations associated & their details
    #http://jacquev6.net/PyGithub/v1/github_objects/Organization.html#github.Organization.Organization
    def fetch_all_orgs_data(self):
        #print "fetch_all_orgs_data is running..."
        organizationDataList = {}

        organizations_count = 0

        try:


            for organization in user.get_orgs():
                organizations_count += 1
                
                tempOrganizationList = {}


                tempOrganizationList['name'] = organization.name
                tempOrganizationList['login'] = organization.login
                tempOrganizationList['collaborators_count'] = organization.collaborators
                tempOrganizationList['company'] = organization.company
                tempOrganizationList['created_at'] = organization.created_at
                tempOrganizationList['email'] = organization.email
                tempOrganizationList['followers_count'] = organization.followers
                tempOrganizationList['html_url'] = organization.html_url
                tempOrganizationList['location'] = organization.location
                tempOrganizationList['repos_private_count'] = organization.owned_private_repos
                tempOrganizationList['repos_public_count'] = organization.public_repos
                tempOrganizationList['type'] = organization.type
                tempOrganizationList['avatar_url'] = organization.avatar_url

                
                for key,value in tempOrganizationList.iteritems():
                    if(key == 'collaborators_count'):
                        tempOrganizationList[key] = 0
                    elif(key == 'repos_private_count'):
                        tempOrganizationList[key] = 0
                    elif(value == None):
                        #print "%s is null" % key
                        tempOrganizationList[key] = NoneReplacement
                

                organizationDataList[organizations_count] = tempOrganizationList


        except UnknownObjectException,e:
            #this is to bypass 404 error received when field is not found
            print "In organization : %s there's an Error : %s " % (str(tempOrganizationList['name']), str(e))
 
        except GithubException,e:
            print "In organization : %s there's an Error : %s " % (str(tempOrganizationList['name']), str(e))
            
        finally:
            return organizationDataList

    
    def fetch_all_repos_data(self):
        #print "fetch_all_repos_data is running..."

        repoDataList = {}
        repos_count = 0
        for repo in user.get_repos():
            if(not repo.private and not repo.fork):
                repos_count += 1
                repoDataList[repos_count] = self.fetch_repo_detail(repo.name)
        

        return repoDataList

    def fetch_repo_detail(self, repo_to_search):
        tempRepoDataList = {}

        try:
            repo = user.get_repo(repo_to_search)

            tempRepoDataList['name'] = repo.full_name
            tempRepoDataList['description'] = repo.description
            tempRepoDataList['created_at'] = repo.created_at
            tempRepoDataList['updated_at'] = repo.updated_at
            tempRepoDataList['html_url'] = repo.html_url
            tempRepoDataList['homepage_url'] = repo.homepage

            languages_dict_ = repo.get_languages()
            languages_values = [{"language_name": k, "language_bytesize": v} for k, v in languages_dict_.items()]
            
            #tempRepoDataList['languages'] = repo.get_languages()
            tempRepoDataList['languages'] = json.dumps(languages_values, indent=4)
            
           

            #tempRepoDataList['contributors_url'] = repo.get_contributors()
            contributors_count = 0
            for contributor in repo.get_contributors():
                contributors_count += 1
            tempRepoDataList['contributors_count'] = contributors_count

            tempRepoDataList['forks_count'] = repo.forks_count
            

            #curl -L https://api.github.com/repos/wahibhaq/android-opencv-lanedetection/tarball > test.targ.gz
            tempRepoDataList['downloads_url'] = repo.get_archive_link('zipball') #other option is tarball
            tempRepoDataList['owner_name'] = repo.owner.name
            tempRepoDataList['watchers_count'] = repo.watchers_count
            tempRepoDataList['size'] = repo.size
            tempRepoDataList['stars_count'] = repo.stargazers_count
            
            try:
                #content can also be fetched in raw(base64 mode) or html
                tempRepoDataList['readme_url'] = repo.get_readme().html_url # shows error if readme missing

            except GithubException,e:
                tempRepoDataList['readme_url'] = NoneReplacement #so that readme_url has None at least in case of error due to missing

                #print "In repo : %s there's an Error : %s " % (str(repo_to_search), str(e))
                pass

            
            try:
                #difference between collaborator and contributer http://bit.ly/1A4alhn
                collaborators_count = 0
                for collaborator in repo.get_collaborators():
                    collaborators_count += 1
                tempRepoDataList['collaborators_count'] = collaborators_count
            except GithubException,e:
                #print "exception in collaborator"
                tempRepoDataList['collaborators_count'] = collaborators_count
                #print "In repo : %s there's an Error : %s " % (str(repo_to_search), str(e))
                pass
                
            


           
            for key,value in tempRepoDataList.iteritems():
                if(value == None):
                    #print "%s is null" % key
                    tempRepoDataList[key] = NoneReplacement

             

        except UnknownObjectException,e:
            #this is to bypass 404 error received when readme is not found in a repo
            print "In repo : %s there's an Error : %s " % (str(repo_to_search), str(e))
            pass

        except GithubException,e:
            print "In repo : %s there's an Error : %s " % (str(repo_to_search), str(e))


        finally:
            return tempRepoDataList
    


    

