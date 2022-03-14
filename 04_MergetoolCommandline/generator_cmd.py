import cmd
import pynames

class NamesGenerator(cmd.Cmd):
    prompt = '> '

    language = pynames.LANGUAGE.NATIVE

    genders = {
        'male': pynames.GENDER.MALE,
        'female': pynames.GENDER.FEMALE
    }

    generators = {}
    for generator in pynames.get_all_generators():
        name = generator.__name__
        subclass = name.removesuffix('NamesGenerator') \
                    .removesuffix('FullnameGenerator') \
                    .removesuffix('Generator')         \
                    .lower()
        main_class = generator.__module__.split('.')[-1]
        if subclass == main_class or main_class == 'russian':
            generators[main_class] = generator
        else:
            if not generators.get(main_class):
                generators[main_class] = {}
            generators[main_class][subclass] = generator
    

    def do_language(self, arg):
        """Set language"""

        lang = arg.split()[0].lower()

        if lang in pynames.LANGUAGE.ALL:
            self.language = lang
        else:
            print(f'Language must be in [{", ".join(pynames.LANGUAGE.ALL)}]')
    

    def complete_language(self, text, line, begidx, endidx):

        return [lang for lang in pynames.LANGUAGE.ALL if lang.startswith(text)]


    def do_generate(self, arg):
        """Generate name of class [subclass] [gender]"""

        args = arg.split()

        if len(args) > 3:
            print('Too many arguments')
            return

        main_class_value = self.generators.get(args[0]) if args else None

        if not main_class_value:
            print('Class does not exist')
            return
        
        flag_subclass = False

        if isinstance(main_class_value, dict):
            if len(args) == 1 or args[1] in self.genders:
                generator = main_class_value[next(iter(main_class_value))]
            elif args[1] not in main_class_value:
                print('Subclass does not exist')
                return
            else:
                generator = main_class_value[args[1]]
                flag_subclass = True
        else:
            generator = main_class_value

        if args[-1] in self.genders:
            gender = self.genders[args[-1]] 
        elif len(args) == 2 and flag_subclass or len(args) == 1:
            gender = self.genders['male']
        else:
            print('Gender does not exist')
            return

        print(generator().get_name_simple(gender, self.language))
    

    def complete_generate(self, text, line, begidx, endidx):

        args = line[:begidx].split()
        
        if len(args) == 1:
            return [cl for cl in self.generators if cl.startswith(text)]

        flag_subclass = isinstance(self.generators.get(args[1]), dict)

        final_generators = []
        if len(args) == 2:
            final_generators += list(self.genders.keys())
            if flag_subclass:
                final_generators += list(self.generators[args[1]].keys())
        elif len(args) == 3 and flag_subclass \
                            and args[2] in self.generators[args[1]].keys():
            final_generators += list(self.genders.keys())

        return [item for item in final_generators if item.startswith(text)]
    

    def do_info(self, arg):
        """Get info"""

        args = arg.split()

        if len(args) > 3:
            print('Too many arguments')
            return

        main_class_value = self.generators.get(args[0]) if args else None

        if not main_class_value:
            print('Class does not exist')
            return

        flag_subclass = False

        if isinstance(main_class_value, dict):
            if len(args) == 1 or args[1] in self.genders:
                print(f'Subclass is not chosen\nAvailable subclasses: '
                      f'{", ".join(self.generators[args[0]])}.')
                return
            elif args[1] not in main_class_value:
                print('Subclass does not exist')
                return
            else:
                generator = main_class_value[args[1]]
                flag_subclass = True
        else:
            generator = main_class_value

        if args[-1] in self.genders:
            gender = self.genders[args[-1]]
            print(generator().get_names_number(gender))
            return
        
        if args[-1] == "language":
            print(*generator().languages)
            return

        if len(args) == 3 or len(args) == 2 and flag_subclass == False:
            print('Wrong last operand, try "language" or "male"/"female"')
            return 

        print(generator().get_names_number())


    def complete_info(self, text, line, begidx, endidx):
        args = line[:begidx].split()
        
        if len(args) == 1:
            return [cl for cl in self.generators if cl.startswith(text)]

        flag_subclass = isinstance(self.generators.get(args[1]), dict)

        if len(args) == 2 and flag_subclass:
            final_generators = list(self.generators[args[1]].keys())
            return [item for item in final_generators if item.startswith(text)]
        
        if len(args) == 2 and not flag_subclass \
           or len(args) == 3 and flag_subclass:
            final_generators = list(self.genders.keys()) + ['language']
            return [item for item in final_generators if item.startswith(text)]


    def do_exit(self, arg):
        """Exit name generation:  exit"""

        return True

NamesGenerator().cmdloop()