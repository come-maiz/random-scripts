require 'find'
require 'json'

if ARGV.length != 2
  puts 'Missing argument.'
  puts 'Usage: ruby top_reaction.rb <path-to-slack-export> <reaction>'
  exit
end

path = ARGV[0]
reaction_name = ARGV[1]

top_count = 0
top_messages = []

Find.find(path) do |file|
  if File.extname(file) == '.json'
    begin
      parsed_json = JSON.parse(File.read(file))
      parsed_json.each do |message|
        if message['type'] == 'message'
          message['reactions'].each do |reaction|
            if reaction['name'] == reaction_name
              reaction_count = reaction['count']
              if reaction_count == top_count
                top_messages.push(message['text'])
              elsif reaction_count > top_count
                top_count = reaction_count
                top_messages = [message['text']]
              end
            end
          end
        end
      end
    rescue => e
    end
  end
end

puts top_count
puts top_messages
