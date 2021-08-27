import sqlite3
import pandas as pd

#----------------------------------------------------------------------------------------------------


#filtered database
res_filtered = './output/res_filtered.db'
db = sqlite3.connect(res_filtered)

db.executescript('''
    CREATE TABLE IF NOT EXISTS repo 
    ( repo_id INTEGER PRIMARY KEY
    , name TEXT NOT NULL
    , full_name TEXT NOT NULL
    , description TEXT
    , url TEXT NOT NULL
    , fork INTEGER NOT NULL
    , owner_id INTEGER NOT NULL
    , owner_login TEXT NOT NULL
    , license TEXT
    );
    CREATE TABLE IF NOT EXISTS file
    ( file_id INTEGER PRIMARY KEY
    , name TEXT NOT NULL
    , path TEXT NOT NULL
    , size INTEGER NOT NULL
    , sha TEXT NOT NULL
    , content TEXT NOT NULL
    , repo_id INTEGER NOT NULL
    , FOREIGN KEY (repo_id) REFERENCES repo(repo_id)
    , UNIQUE(path,repo_id)
    );

    ''')

db.executescript('''
    CREATE TABLE IF NOT EXISTS git_commit
    ( commit_id INTEGER PRIMARY KEY
    , message TEXT NOT NULL
    , author TEXT NOT NULL
    , url TEXT NOT NULL
    , total INTEGER NOT NULL
    , additions INTEGER NOT NULL
    , deletions INTEGER NOT NULL
    , sha TEXT NOT NULL
    , repo_id INTEGER NOT NULL
    , FOREIGN KEY (repo_id) REFERENCES repo(repo_id)
    , UNIQUE(url,repo_id)
    );
    CREATE TABLE IF NOT EXISTS commit_content
    ( content_id INTEGER PRIMARY KEY
    , file_name TEXT NOT NULL
    , sha TEXT NOT NULL
    , status TEXT NOT NULL
    , additions INTEGER NOT NULL
    , deletions TEXT NOT NULL
    , changes INTEGER NOT NULL
    , contents_url TEXT NOT NULL
    , content TEXT NOT NULL
    , commit_id INTEGER NOT NULL
    , FOREIGN KEY (commit_id) REFERENCES git_commit(commit_id)
    , UNIQUE (commit_id,contents_url)
    ); 
    ''')

def insert_repo(repo):
    db.execute('''
        INSERT OR IGNORE INTO repo 
            ( repo_id, name, full_name, description, url, fork
            , owner_id, owner_login, license
            )
        VALUES (?,?,?,?,?,?,?,?,?)
        ''',
        ( repo[0]
        , repo[1]
        , repo[2]
        , repo[3]
        , repo[4]
        , repo[5]
        , repo[6]
        , repo[7]
        , repo[8]
        )
        )
    db.commit()
    

def insert_file(file):
    db.execute('''
        INSERT OR IGNORE INTO file
            (file_id, name, path, size, sha, content, repo_id)
        VALUES (?,?,?,?,?,?,?)
        ''',
        ( file[0]
        , file[1]
        , file[2]
        , file[3]
        , file[4]
        ,file[5]
        , file[6]
        ))
    db.commit()

def insert_git_commit(git_commit):
    db.execute('''
        INSERT OR IGNORE INTO git_commit
            (commit_id, message, author, url, total, additions, deletions, sha, repo_id)
        VALUES(?,?,?,?,?,?,?,?,?)
        ''', 
        (git_commit[0]
        , git_commit[1]
        , git_commit[2]
        , git_commit[3]
        , git_commit[4]
        , git_commit[5]
        , git_commit[6]
        , git_commit[7]
        , git_commit[8]
        ))
    db.commit()

def insert_commit_content(commit_content):
    db.execute('''
        INSERT OR IGNORE INTO commit_content
            (content_id, file_name, sha, status, additions, deletions, changes, contents_url, content, commit_id)
            VALUES(?,?,?,?,?,?,?,?,?,?)
        ''',
        (commit_content[0]
        , commit_content[1]
        , commit_content[2]
        , commit_content[3]
        , commit_content[4]
        , commit_content[5]
        , commit_content[6]
        , commit_content[7]
        , commit_content[8]
        , commit_content[9]
        ))
    db.commit()   


#connect to the unfiltered database
database = './output/res.db'
con = sqlite3.connect(database)
cur = con.cursor()
db_cur = db.cursor()

# reading all table names
table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
# here is you table list
print(table_list)

# one of the files of the ch.tuw.githubsearcher.repository contains pragma
repos = [a for a in cur.execute("Select repo_id FROM file WHERE content LIKE '%pragma solidity%' OR content LIKE '% contract%'")]
for id in repos:
    repo =[a for a in  cur.execute("Select * from repo WHERE repo_id = ?", 
    (id))]
    insert_repo(repo[0])
    files = [a for a in cur.execute("SELECT * FROM file WHERE repo_id =?", 
    (id))]
    #insert all files of this ch.tuw.githubsearcher.repository
    for file in files: 
        insert_file(file)
    commits = [a for a in cur.execute("SELECT * FROM git_commit WHERE repo_id = ?", 
    (id))] 
    #insert all commits for this ch.tuw.githubsearcher.repository
    for commit in commits:
        insert_git_commit(commit)
        commit_id = commit[0]
        commit_contents = [a for a in cur.execute("SELECT * FROM commit_content WHERE commit_id =?",(commit_id,))] 
        for content in commit_contents:
          insert_commit_content(content) 
        



# Be sure to close the connection
con.close()
db.close()

        
