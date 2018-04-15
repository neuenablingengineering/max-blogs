# -*- coding: utf-8 -*-

import sys
import os
import time
import blogger_connector
from oauth2client import client
from googleapiclient import sample_tools


def main(argv):
    service, flags = sample_tools.init(argv, 'blogger', 'v3', __doc__, __file__,
                                       scope='https://www.googleapis.com/auth/blogger')
    users = service.users()
    blogs = service.blogs()
    posts = service.posts()

    path_to_watch = "."
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
        time.sleep (5)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        new = [f for f in after if not f in before]
        if new:
            try:
                file_list = parse_files(new)
                # Retrieve the list of Blogs this user has write privileges on
                this_users_blogs = blogs.listByUser(userId='self').execute()
                for blog in this_users_blogs['items']:
                    id = blog['id']
                for key in file_list:
                    if file_list[key] != "":

                        # Setup content format
                        content = blogger_connector.content_setup(id, key[:-4], file_list[key])
                        # Publish a draft page
                        new_post = blogger_connector.create_draft_post(posts, id, content)
                        print(new_post)

            except client.AccessTokenRefreshError:
                print('The credentials have been revoked or expired, please re-run'
                      'the application to re-authorize')
        before = after


def get_files(path):
    file_list = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            file_list.append(file)

    return ",".join(file_list)


def parse_files(files):
    file_list = {}
    for f in files:
        with open(f, 'r') as myfile:
            body = "<div>"
            body += myfile.read() + "</div>"
            file_list[f] = body

    return file_list


def parse_logfile():
    with open("log.txt", "r") as logfile:
        return logfile.read().split(",")


def save_logfile(files):
    logfile = open("log.txt", "w")
    logfile.write(",".join(files))


if __name__ == '__main__':
    main(sys.argv)