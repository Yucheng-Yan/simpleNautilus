class User():
    def __init__(self, id):
        self.id = id
    
    #functional functions
    def adduser(id, user_dict):
        for user in user_dict:
            if user == id:
                print("adduser: The user already exists")
                return
        new_user = User(id)
        user_dict[id] = new_user

    def deluser(id, user_dict):
        if id == "root":
            print("WARNING: You are just about to delete the root account\nUsually this is never required as it may render the whole system unusable\nIf you really want this, call deluser with parameter --force\n(but this `deluser` does not allow `--force`, haha)\nStopping now without having performed any action")
        for user in user_dict:
            if user == id:
                del user_dict[user]
                return
        print("deluser: The user does not exist")
    
    def su(id, user_dict):
        for user in user_dict:
            if user == id:
                return user_dict[id]
        print("su: Invalid user")
        return None
            
    def su_without_user(user_dict):
        return user_dict["root"]
    
    
class File():
    def __init__(self, user, name):
        self.user = user
        self.name = name
        self.parent = {}
        self.permission = ['r', 'w', '-', 'r', '-', '-']
        
    #helper functions
    def get_parent_name_ls(self):
        """Generate a list consists of the name of ancestors."""
        return list(self.parent.keys())
    
    def add_parent(self, dir):
        """Add a child to self.
        
        Keyword argument:
        :param dir(dir) -- the parent of self"""
        self.parent.update(dir.parent)
        self.parent[dir.name] = dir
        
    def is_a_file(self):
        """To show this obj is a file"""
        return True
    
    def get_permission(self):
        """Return the permission of self in a ls -l way"""
        permission = ['-'] + self.permission
        return ''.join(permission)
    
    def set_permission(self, permission):
        """Set the permission of self"""
        self.permission = permission
        




class Directory():
    def __init__(self, user, name):
        self.user = user
        self.name = name
        self.parent = {}
        self.child = {}
        self.permission = ['r', 'w', 'x', 'r', '-', 'x']
    
    #helper functions
    def get_parent_name_ls(self):
        """Generate a list consists of the name of ancestors."""
        return list(self.parent.keys())
    
    def get_child_name_ls(self):
        """Generate a list consists of the name of child."""
        return list(self.child.keys())
    
    def add_child(self, dir): 
        """Add a child to self.
        
        Keyword argument:
        :param dir(dir) -- the new child of self"""
        self.child[dir.name] = dir
        
    def add_parent(self, dir):
        """Add a child to self.
        
        Keyword argument:
        :param dir(dir) -- the parent of self"""
        self.parent.update(dir.parent)
        self.parent[dir.name] = dir
    
    def get_permission(self):
        """Return the permission of self in a ls -l way"""
        permission = ['d'] + self.permission
        return ''.join(permission)
        
    def path_checker(self, dir, cur):
        """Nevigating through the path and see if it is valid.
        
        Keyword arguments:
        :param dir(str) -- the path of destination directory
        :param cur(dir) -- the current cursor directory
        :return: if it is suitable to create a new dir, which is the one at the last position of dir
        """
        ls = dir.split('/')
        counter = 0
        if (ls[0] == '.' or 
            ls[0] == '..' or 
            ls[0] == '' or #start with /
            ls[0] in cur.get_child_name_ls()): 
            for destination in ls:
                if destination == '.':
                    counter += 1
                elif destination == '..' and cur.name != '/':
                    cur = cur.parent[list(cur.parent.keys())[-1]] 
                    counter += 1
                elif destination =='':
                    counter += 1
                elif destination == '..':
                    counter += 1
                elif str(type(cur)) == "<class '__main__.File'>":
                    return False
                elif destination in cur.get_child_name_ls():
                    counter += 1
                    for child in cur.child:
                        if child == destination:
                            cur = cur.child[child]
        if len(ls) - counter == 1:
            return True #wise to crete a new dir, which is the one at the end of the path
        elif len(ls) - counter == 0:
            return None #the last dir in path already exist
        else:
            return False #some dir in path do not exist yet

    def type_of_the_path(self, dir):
        """Return the data type of <dir>.
        
        Keyword arguments:
        :param dir(str) -- the path of target directory
        :return: the data type of target directory
        """
        cur = self
        if cur.name == '/' and dir == '/':
            return
        elif dir == '/':
            return "directory"
        ls = dir.split('/')
        # the following if statement is needed because return cur is in the same level of indentation, otherwise print statement will never be run
        if (ls[0] == '.' or 
            ls[0] == '..' or 
            ls[0] == '' or #start with /
            ls[0] in cur.get_child_name_ls()): 
            if len(ls) == 1:
                if (ls[0] in cur.get_child_name_ls() and
                    cur.child[ls[0]].is_a_file()):
                    return "file"
                return "directory"
            for destination in ls[:len(ls)-1]: #stop at second last item
                if destination == '.':
                    pass
                elif destination == '..' and cur.name != '/':
                    # set cur as its parent(not ancestor)
                    cur = cur.parent[list(cur.parent.keys())[-1]] 
                elif destination in cur.get_child_name_ls():
                    if cur.child[destination].is_a_file():
                        return "file"
                    for child in cur.child:
                        if child == destination:
                            cur = cur.child[child]
            if (ls[len(ls)-1] in cur.get_child_name_ls() and 
                cur.child[ls[len(ls)-1]].is_a_file()):
                return "file"
            elif (ls[len(ls)-1] in cur.get_child_name_ls() and not 
                cur.child[ls[len(ls)-1]].is_a_file()):
                return "directory"

    def is_empty(self, dir):
        """To judge if <dir> is empty.
        
        Keyword arguments:
        :param dir(str) -- the path of target directory
        :return: if the target directory is empty or not
        """
        cur = self
        if cur.name == '/' and dir == '/':
            if cur.child == {}:
                return True
            else:
                return False
        ls = dir.split('/')
        # the following if statement is needed because return cur is in the same level of indentation, otherwise print statement will never be run
        if (ls[0] == '.' or 
            ls[0] == '..' or 
            ls[0] == '' or #start with /
            ls[0] in cur.get_child_name_ls()): 
            for destination in ls: 
                if destination == '.':
                    pass
                elif destination == '..' and cur.name != '/':
                    # set cur as its parent(not ancestor)
                    cur = cur.parent[list(cur.parent.keys())[-1]] 
                elif destination in cur.get_child_name_ls():
                    for child in cur.child:
                        if child == destination:
                            cur = cur.child[child]
            if cur.child == {}:
                return True
            else:
                return False
            
    def is_pwd(self, dir, cur):
        """To judge if <dir> is pwd.
        
        Keyword arguments:
        :param dir(str) -- the path of target directory
        :param cur(dir) -- the current dir when call the function
        :return: if the target directory is empty or not
        """
        cursor = self
        if dir == '.':
            return True
        elif cur.name == '/' and dir == '/':
            return True
        ls = dir.split('/')
        # the following if statement is needed because return cur is in the same level of indentation, otherwise print statement will never be run
        if (ls[0] == '.' or 
            ls[0] == '..' or 
            ls[0] == '' or #start with /
            ls[0] in cursor.get_child_name_ls()): 
            for destination in ls: 
                if destination == '.':
                    pass
                elif destination == '..' and cursor.name != '/':
                    # set cursor as its parent(not ancestor)
                    cursor = cursor.parent[list(cursor.parent.keys())[-1]] 
                elif destination in cursor.get_child_name_ls():
                    for child in cursor.child:
                        if child == destination:
                            cursor = cursor.child[child]
            # print(">>>After for loop, cursor = " + cursor.name)#
            # print(">>>cur.name = " + cur.name)#
            if cursor.name == cur.name:
                return True
            else:
                return False
            
    def is_a_file(self):
        """To show this obj is not a file"""
        return False
    
    def set_permission(self, permission):
        """Set the permission of self"""
        self.permission = permission
        
    def command_validator(self, command):
        punc = "`~!@#$%^&*()+=[]{}\|;:?<>,"
        for letter in command:
            if (letter in punc or
                letter == ' '):
                return False
        return True

    #functional functions
    def pwd(self, cur):
        """Print working directory of the cursor directory.
        
        Keyword argument:
        :param cur(dir) -- the current cursor directory"""
        parent_name_ls = cur.get_parent_name_ls()
        if parent_name_ls == []:
            print('/')
        else:
            print('/'.join(parent_name_ls)[1:] + '/' + cur.name)
            
    def cd(self, dir, cur, root):
        """Shift the current cursor directory.
        
        Keyword arguments:
        :param dir(str) -- the name of destination directory
        :param cur(dir) -- the current cursor directory
        :param root(dir) -- the root directory
        :return: the new cursor directory(if there is)
        """
        if cur.name == '/' and dir == '/':
            return
        elif dir == '/':
            return root
        ls = dir.split('/')
        cursor = cur
        if (ls[0] == '.' or 
            ls[0] == '..' or 
            ls[0] == '' or #start with /
            ls[0] in cursor.get_child_name_ls()):                 
            for destination in ls:
                if destination == '.':
                    pass
                elif destination == '..' and cursor.name != '/':
                    # set cur as its parent(not ancestor)
                    cursor = cursor.parent[list(cursor.parent.keys())[-1]] 
                elif destination in cursor.get_child_name_ls():
                    if cursor.child[destination].is_a_file():
                        print("cd: Destination is a file")
                    for child in cursor.child:
                        if child == destination:
                            cursor = cursor.child[child]
                elif (destination not in cursor.get_child_name_ls() and 
                      destination != '.' and
                      destination != '..' and 
                      destination != ''):
                    print("cd: No such file or directory")
                    return cur
            return cursor
        else:
            print("cd: No such file or directory")
            return None  
            
    def mkdir(self, arg):
        """Create a new directory, if any ancestor directory in <arg> does not exist, print error message.
        
        Keyword arguments:
        :param arg(str) -- a string consists of the path of dir to be
                           built
        """
        if arg[0] == '/':
            arg = arg[1:]
        if self.path_checker(arg, self) == None:
            print("mkdir: File exists")
        elif self.path_checker(arg, self):
            path_ls = ['/']
            path_ls += arg.split('/')
            cursor = self
            for dir in path_ls[1:]:
                if (dir not in cursor.get_child_name_ls() or
                    str(type(cursor.child[dir])) == "<class '__main__.Directory'>"):
                    dir = Directory(self.user, dir)
                    dir.add_parent(cursor)
                    cursor.add_child(dir)
                    cursor = dir
                else:
                    cursor = cursor.child[dir]
                    continue
        else:
            print("mkdir: Ancestor directory does not exist")
                
    def mkdir_withp(self, arg):
        """Create a new directory, if any ancestor directory in <arg> does not exist, create the ancestor at first.
        
        Keyword arguments:
        :param arg(str) -- a string consists of the path of dir to be built
        """
        if arg[0] == '/':
            arg = arg[1:]
        if self.path_checker(arg, self):
            self.mkdir(arg)
        else:
            path_ls = ['/']
            path_ls += arg.split('/')
            cursor = self
            for dir in path_ls[1:]:
                if (dir not in cursor.get_child_name_ls() or
                    str(type(cursor.child[dir])) == "<class '__main__.Directory'>"):
                    dir = Directory(self.user, dir)
                    dir.add_parent(cursor)
                    cursor.add_child(dir)
                    cursor = dir
                else:
                    cursor = cursor.child[dir]
                    continue
    
    def touch(self, arg):
        """Create a new file.
        
        Keyword arguments:
        :param arg(str) -- a string consists of the path of file to be built
        """
        if arg[0] == '/':
            arg = arg[1:]
        if self.path_checker(arg, self) == None:
            pass
        elif self.path_checker(arg, self) == False:
            print("touch: Ancestor directory does not exist")
        else:
            path_ls = ['/']
            path_ls += arg.split('/')
            cursor = self
            for item in path_ls[1:]:
                if item in cursor.get_child_name_ls():
                    cursor = cursor.child[item]
                    pass
                elif item not in cursor.get_child_name_ls():
                    item = File(self.user, path_ls[len(path_ls)-1])
                    item.add_parent(cursor)
                    cursor.add_child(item)
                    break
                else:
                    cursor = item
                    return
                
    def cp(self, src, dst, cur): 
        """Copy a file from <src> to <dst>.
        
        Keyword arguments:
        :param src(str) -- a string consists of the path of the
                           source file
        :param dst(str) -- a string consists of the path of the
                           destination file
        :param cur(dir) -- the current directory
        """
        if self.path_checker(src, self) == False:
            print("cp: No such file")
        elif self.type_of_the_path(dst) == "directory":
            print("cp: Destination is a directory")
        elif self.type_of_the_path(src) == "directory":
            print("cp: Source is a directory")
        elif self.path_checker(dst, self) == None:
            print("cp: File exists")
        elif self.path_checker(src, self) == True:
            print("cp: No such file")
        elif self.path_checker(dst, self) == False:
            print("cp: No such file or directory")
        else:
            cursor = cur
            src = src.split('/')
            if (src[0] == '.' or 
                src[0] == '..' or 
                src[0] == '' or #start with /
                src[0] in cursor.get_child_name_ls()): 
                for destination in src[:len(src)-1]: # here the main purpose is for iterating the cursor
                    if destination == '.':
                        pass
                    elif destination == '..' and cursor.name != '/':
                        cursor = cursor.parent[list(cursor.parent.keys())[-1]] 
                    elif destination in cursor.get_child_name_ls():
                        for child in cursor.child:
                            if child == destination:
                                cursor = cursor.child[child]
                if src[len(src)-1] in cursor.get_child_name_ls():
                    file_to_move = cursor.child[src[len(src)-1]]
            dst = dst.split('/')        
            if ([0] == '.' or 
                dst[0] == '..' or 
                dst[0] == '' or #start with /
                dst[0] in cur.get_child_name_ls()): 
                for destination in dst[:len(dst)-1]: # here the main purpose is for iterating the cursor
                    if destination == '.':
                        pass
                    elif destination == '..' and cur.name != '/':
                        cur = cur.parent[list(cur.parent.keys())[-1]] 
                    elif destination in cur.get_child_name_ls():
                        for child in cur.child:
                            if child == destination:
                                cur = cur.child[child]
                cur.child[dst[len(dst)-1]] = file_to_move
            
    def mv(self, src, dst, cur): 
        """Move a file from <src> to <dst>.
        
        Keyword arguments:
        :param src(str) -- a string consists of the path of the
                           source file
        :param dst(str) -- a string consists of the path of the
                           destination file
        :param cur(dir) -- the current directory
        """
        if self.path_checker(src, self) == False:
            print("mv: No such file")
        elif self.type_of_the_path(dst) == "directory":
            print("mv: Destination is a directory")
        elif self.type_of_the_path(src) == "directory":
            print("mv: Source is a directory")
        elif self.path_checker(dst, self) == None:
            print("mv: File exists")
        elif self.path_checker(src, self) == True:
            print("mv: No such file")
        elif self.path_checker(dst, self) == False:
            print("mv: No such file or directory")
        else:
            cursor = cur
            src = src.split('/')
            if (src[0] == '.' or 
                src[0] == '..' or 
                src[0] == '' or #start with /
                src[0] in cursor.get_child_name_ls()): 
                for destination in src[:len(src)-1]: # here the main purpose is for iterating the cursor
                    if destination == '.':
                        pass
                    elif destination == '..' and cursor.name != '/':
                        cursor = cursor.parent[list(cursor.parent.keys())[-1]] 
                    elif destination in cursor.get_child_name_ls():
                        for child in cursor.child:
                            if child == destination:
                                cursor = cursor.child[child]
                if src[len(src)-1] in cursor.get_child_name_ls():
                    file_to_move = cursor.child[src[len(src)-1]]
                    del cursor.child[src[len(src)-1]]
            dst = dst.split('/')        
            if ([0] == '.' or 
                dst[0] == '..' or 
                dst[0] == '' or #start with /
                dst[0] in cur.get_child_name_ls()): 
                for destination in dst[:len(dst)-1]: # here the main purpose is for iterating the cursor
                    if destination == '.':
                        pass
                    elif destination == '..' and cur.name != '/':
                        cur = cur.parent[list(cur.parent.keys())[-1]] 
                    elif destination in cur.get_child_name_ls():
                        for child in cur.child:
                            if child == destination:
                                cur = cur.child[child]
                cur.child[dst[len(dst)-1]] = file_to_move
        
    def rm(self, path, cur): 
        """remove a file in the <path>.
        
        Keyword arguments:
        :param path(str) -- a string consists of the path of the
                           target file
        :param cur(dir) -- the current directory
        """
        if self.type_of_the_path(path) == "directory":
            print("rm: Is a directory")
        elif self.path_checker(path, self) == None:
            cursor = cur
            path = path.split('/')
            if (path[0] == '.' or 
                path[0] == '..' or 
                path[0] == '' or #start with /
                path[0] in cursor.get_child_name_ls()): 
                for destination in path[:len(path)-1]: # here the main purpose is for iterating the cursor
                    if destination == '.':
                        pass
                    elif destination == '..' and cursor.name != '/':
                        cursor = cursor.parent[list(cursor.parent.keys())[-1]] 
                    elif destination in cursor.get_child_name_ls():
                        for child in cursor.child:
                            if child == destination:
                                cursor = cursor.child[child]
                if path[len(path)-1] in cursor.get_child_name_ls():
                    del cursor.child[path[len(path)-1]]
        else:
            print("rm: No such file")
        
    def rmdir(self, dir, cur): 
        """remove a file in the <path>.
        
        Keyword arguments:
        :param dir(str) -- a string consists of the path of the
                           target directory
        :param cur(dir) -- the current directory when call this function
        """
        # print(">>>is_pwd(): " + str(self.is_pwd(dir, cur)))#
        if self.type_of_the_path(dir) == "file":
            print("rmdir: Not a directory")
        elif self.is_pwd(dir, cur):
            print("rmdir: Cannot remove pwd")
        elif ((self.path_checker(dir, self) == None and 
              self.is_empty(dir) == False)):
            print("rmdir: Directory not empty")
        elif (self.path_checker(dir, self) == None and
              self.type_of_the_path(dir) == "directory"):
            cursor = cur
            dir = dir.split('/')
            if (dir[0] == '.' or 
                dir[0] == '..' or 
                dir[0] == '' or #start with /
                dir[0] in cursor.get_child_name_ls()): 
                for destination in dir[:len(dir)-1]: # here the main purpose is for iterating the cursor
                    if destination == '.':
                        pass
                    elif destination == '..' and cursor.name != '/':
                        cursor = cursor.parent[list(cursor.parent.keys())[-1]] 
                    elif destination in cursor.get_child_name_ls():
                        for child in cursor.child:
                            if child == destination:
                                cursor = cursor.child[child]
                if dir[len(dir)-1] in cursor.get_child_name_ls():
                    del cursor.child[dir[len(dir)-1]]
        else:
            print("rmdir: No such file or directory")
        
    def ls(self, flag, cur):
        
        if flag == None:
            ls = []
            for child in cur.get_child_name_ls():
                ls.append(child)
            ls.sort()
            print(' '.join(ls))
        elif flag == "-l":
            for child in cur.child:
                print(cur.child[child].get_permission(), end='')
                print(' ' + cur.child[child].user.id, end='')
                print(' ' + cur.child[child].name)

    def chmod(self, equation, path, cur):
        for child in cur.get_child_name_ls():
            if child == path:
                permission = cur.child[child].permission
                if len(equation)==2:
                    if equation[0] == 'a':
                        permission = ['-', '-', '-', '-', '-', '-']
                        cur.child[child].set_permission(permission)
                    elif equation[0] == 'u':
                        permission = ['-', '-', '-'] + permission[3:]
                        cur.child[child].set_permission(permission)
                    elif equation[0] == 'o':
                        permission = permission[:3] + ['-', '-', '-']
                        cur.child[child].set_permission(permission)
                elif len(equation)==3:
                    if equation[0] == 'a':
                        if equation[1] == "+":
                            if equation[2] == "r":
                                permission = (['r'] + list(permission[1]) + list(permission[2]) + 
                                              ['r'] + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "w":
                                permission = (list(permission[0]) + ['w'] + list(permission[2]) + 
                                              list(permission[3]) + ['w'] + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "x":
                                permission = (list(permission[0]) + list(permission[1]) + ['x'] + 
                                              list(permission[3]) + list(permission[4]) + ['x'])
                                cur.child[child].set_permission(permission)
                        elif equation[1] == "-":
                            if equation[2] == "r":
                                permission = (['-'] + list(permission[1]) + list(permission[2]) + 
                                              ['-'] + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "w":
                                permission = (list(permission[0]) + ['-'] + list(permission[2]) + 
                                              list(permission[3]) + ['-'] + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "x":
                                permission = (list(permission[0]) + list(permission[1]) + ['-'] + 
                                              list(permission[3]) + list(permission[4]) + ['-'])
                                cur.child[child].set_permission(permission)
                        elif equation[1] == "=":
                            if equation[2] == "r":
                                permission = (['r'] + ['-'] + ['-'] + 
                                              ['r'] + ['-'] + ['-'])
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "w":
                                permission = (['-'] + ['w'] + ['-'] + 
                                              ['-'] + ['w'] + ['-'])
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "x":
                                permission = (['-'] + ['-'] + ['x'] + 
                                              ['-'] + ['-'] + ['x'])
                                cur.child[child].set_permission(permission)
                    elif equation[0] == 'u':  
                        if equation[1] == "+":
                            if equation[2] == "r":
                                permission = (['r'] + list(permission[1]) + list(permission[2]) +
                                              list(permission[3]) + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "w":
                                permission = (list(permission[0]) + ['w'] + list(permission[2]) +
                                              list(permission[3]) + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "x":
                                permission = (list(permission[0]) + list(permission[1]) + ['x'] +
                                              list(permission[3]) + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                        elif equation[1] == "-":
                            if equation[2] == "r":
                                permission = (['-'] + list(permission[1]) + list(permission[2]) +
                                              list(permission[3]) + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "w":
                                permission = (list(permission[0]) + ['-'] + list(permission[2]) +
                                              list(permission[3]) + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "x":
                                permission = (list(permission[0]) + list(permission[1]) + ['-'] +
                                              list(permission[3]) + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                        elif equation[1] == "=":
                            if equation[2] == "r":
                                permission = (['r'] + ['-'] + ['-'] +
                                              list(permission[3]) + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "w":
                                permission = (['-'] + ['w'] + ['-'] +
                                              list(permission[3]) + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "x":
                                permission = (['-'] + ['-'] + ['x'] +
                                              list(permission[3]) + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                    elif equation[0] == 'o':
                        if equation[1] == "+":
                            if equation[2] == "r":
                                permission = (list(permission[0]) + list(permission[1]) + list(permission[2]) +
                                              ['r'] + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "w":
                                permission = (list(permission[0]) + list(permission[1]) + list(permission[2]) +
                                              list(permission[3]) + ['w'] + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "x":
                                permission = (list(permission[0]) + list(permission[1]) + list(permission[2]) +
                                              list(permission[3]) + list(permission[4]) + ['x'])
                                cur.child[child].set_permission(permission)
                        elif equation[1] == "-":
                            if equation[2] == "r":
                                permission = (list(permission[0]) + list(permission[1]) + list(permission[2]) +
                                              ['-'] + list(permission[4]) + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "w":
                                permission = (list(permission[0]) + list(permission[1]) + list(permission[2]) +
                                              list(permission[3]) + ['-'] + list(permission[5]))
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "x":
                                permission = (list(permission[0]) + list(permission[1]) + list(permission[2]) +
                                              list(permission[3]) + list(permission[4]) + ['-'])
                                cur.child[child].set_permission(permission)
                        elif equation[1] == "=":
                            if equation[2] == "r":
                                permission = (list(permission[0]) + list(permission[1]) + list(permission[2]) +
                                              ['r'] + ['-'] + ['-'])
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "w":
                                permission = (list(permission[0]) + list(permission[1]) + list(permission[2]) +
                                              ['-'] + ['w'] + ['-'])
                                cur.child[child].set_permission(permission)
                            elif equation[2] == "x":
                                permission = (list(permission[0]) + list(permission[1]) + list(permission[2]) +
                                              ['-'] + ['-'] + ['x'])
                                cur.child[child].set_permission(permission)
        return cur        
    
    def chown(self, user, path, cur, user_dict):
        if user not in user_dict:
            print("chown: Invalid user")
            return
        elif path not in cur.get_child_name_ls():
            print("chown: No such file or directory")
            return
        elif self.user.id != "root":
            print("chown: Operation not permitted")
        else:
            for child in cur.child:
                if child == path:
                    cur.child[child].user = user_dict[user]
                
    def prompt(self, cur, root, user_dict):  
        #only check the number of arguments within this method
        parent_name_ls = cur.get_parent_name_ls()
                    
        if parent_name_ls == []:   
            print(cur.user.id + ":" + '/' + '$ ', end='')
        else:
            print_value = '/'.join(parent_name_ls[1:]) + '/' + cur.name + '$ '
            if print_value[0] != '/':
                print_v = cur.user.id + ":" + '/'
                print_v += print_value
                print(print_v, end='')
            else:
                print(cur.user.id + ":" + '/'.join(parent_name_ls[1:]) + '/' + cur.name + '$ ', end='')
        command = input()
        output = System(command)
        if command == '':
            return
        #pwd 
        elif command.split()[0] == "pwd":
            if len(command.split()) != 1:
                output.invalid_syntax()
                return
            self.pwd(cur)
            return
        #cd
        elif command.split()[0] == "cd":
            if len(command.split()) != 2:
                output.invalid_syntax()
                return
            else:
                return(self.cd(command.split()[1], cur, root))
        #mkdir
        elif command.split()[0] == "mkdir":
            if len(command.split()) == 2:
                if not self.command_validator(command.split()[1]):
                    output.invalid_syntax()
                    return
                cur.mkdir(command.split()[1])
            elif (len(command.split()) == 3 and
                  command.split()[1] == '-p'):
                if not self.command_validator(command.split()[2]):
                    output.invalid_syntax()
                    return
                cur.mkdir_withp(command.split()[2])
            else:
                output.invalid_syntax()
                return
        #touch
        elif command.split()[0] == "touch":
            if len(command.split()) != 2:
                output.invalid_syntax()
                return
            else:
                if not self.command_validator(command.split()[1]):#
                    output.invalid_syntax()
                    return
                return(self.touch(command.split()[1]))
        #cp
        elif command.split()[0] == "cp":
            if len(command.split()) != 3:
                output.invalid_syntax()
                return
            else:
                if not self.command_validator(command.split()[1]):#
                    output.invalid_syntax()
                    return
                if not self.command_validator(command.split()[2]):#
                    output.invalid_syntax()
                    return
                src = command.split()[1]
                dst = command.split()[2]
                self.cp(src, dst, cur)
        #mv
        elif command.split()[0] == "mv":
            if len(command.split()) != 3:
                output.invalid_syntax()
                return
            else:
                if not self.command_validator(command.split()[1]):#
                    output.invalid_syntax()
                    return
                if not self.command_validator(command.split()[2]):#
                    output.invalid_syntax()
                    return
                src = command.split()[1]
                dst = command.split()[2]
                self.mv(src, dst, cur)
        #rm
        elif command.split()[0] == "rm":
            if len(command.split()) != 2:
                output.invalid_syntax()
                return
            else:
                if not self.command_validator(command.split()[1]):#
                    output.invalid_syntax()
                    return
                path = command.split()[1]
                self.rm(path, cur)                
        #rmdir
        elif command.split()[0] == "rmdir":
            if len(command.split()) != 2:
                output.invalid_syntax()
                return
            else:
                if not self.command_validator(command.split()[1]):#
                    output.invalid_syntax()
                    return
                dir = command.split()[1]
                self.rmdir(dir, cur)
                
        #adduser
        elif command.split()[0] == "adduser":
            if len(command.split()) != 2:
                output.invalid_syntax()
                return
            else:
                new_id = command.split()[1]
                User.adduser(new_id, user_dict)
        
        #adduser
        elif command.split()[0] == "deluser":
            if len(command.split()) != 2:
                output.invalid_syntax()
                return
            else:
                to_be_del = command.split()[1]
                User.deluser(to_be_del, user_dict)

        
        #su
        elif command.split()[0] == "su":
            if len(command.split()) == 2:
                return_user = User.su(command.split()[1], user_dict)
                if return_user == None:
                    pass
                else:
                    self.user = User.su(command.split()[1], user_dict)
            elif len(command.split()) == 1:
                self.user = User.su_without_user(user_dict)
            else:
                output.invalid_syntax()
                return

        #ls -l
        elif command.split()[0] == "ls":
            if len(command.split()) > 5:
                output.invalid_syntax()
            elif len(command.split()) == 1:
                cur.ls(None, cur)
            elif (len(command.split()) == 2 and
                  command.split()[1] == "-l"):
                cur.ls(command.split()[1], cur)

        #chmod
        elif command.split()[0] == "chmod":
            if len(command.split()) > 4:
                output.invalid_syntax()
            elif command.split()[1] == "-r":
                pass
            else:
                equation = command.split()[1]
                path = command.split()[2]
                return(self.chmod(equation, path, cur))
        
        #chown
        elif command.split()[0] == "chown":
            if len(command.split()) > 4:
                output.invalid_syntax()
            elif command.split()[1] == "-r":
                pass
            else:
                user = command.split()[1]
                path = command.split()[2]
                return(self.chown(user, path, cur, user_dict))
            

        elif command.split()[0] == "exit":
            if(len(command.split())) != 1:
                output.invalid_syntax()
            else:
                return 0
        
        else:
            output.command_not_found()
            return


class System():
    def __init__(self, command):
        self.command = command
        
    def command_not_found(self):
        print(self.command + ": Command not found")
    
    def invalid_syntax(self):
        print(self.command.split()[0] + ': Invalid syntax')
          
          
def main():    
    user_dict = {}
    root = User("root")
    user_dict["root"] = root
    init_directory = Directory(root, '/')
    cursor_dir = init_directory
    
    while True:
        #print(">>>cursor_dir.permission = " + str(cursor_dir.permission))
        return_value = init_directory.prompt(cursor_dir, init_directory, user_dict)
        if isinstance(return_value, Directory):
            #change the cursor caused by cd etc
            cursor_dir = return_value 
            continue
        elif return_value == 0:
            print("bye,", init_directory.user.id)
            break


if __name__ == '__main__':
    main()
    