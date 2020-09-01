require 'find'
require 'json'

if ARGV.length < 1
  puts 'Missing argument.'
  puts 'Usage: ruby top_reaction.rb <path-to-slack-export> <reactions>'
  exit
end

AWARDS = %w(award_for_ability_to_ship award_for_healthy_workstyle award_for_intellectual_curiosity award_for_strong_sense_of_purpose award_for_commitment_to_excellence award_for_team_spirit thankyou-nico cv_whateverittakes)

path = ARGV[0]
reaction_names = ARGV[1] ? ARGV[1].split(/\s+/) : AWARDS

def msg_to_text(message, file)
  sender = message['user_profile'].nil? ? 'unknown' : message['user_profile']['name']
  "from #{sender} in #{file.split('/')[-2]} on #{File.basename(file, '.json')}\n\n#{message['text']}"
end

def stats(path, reaction_name)
  top_count = 0
  top_messages = []

  Find.find(path) do |file|
    if File.extname(file) == '.json'
      begin
        parsed_json = JSON.parse(File.read(file))
        parsed_json.each do |message|
          if message['type'] == 'message'
            if !message['reactions'].nil?
              message['reactions'].each do |reaction|
                if reaction['name'] == reaction_name
                  reaction_count = reaction['count']
                  if reaction_count == top_count
                    top_messages.push(msg_to_text(message, file))
                  elsif reaction_count > top_count
                    top_count = reaction_count
                    top_messages = [msg_to_text(message, file)]
                  end
                end
              end
            end
          end
        end
      rescue => e
        puts e
      end
    end
  end

  [top_count, top_messages]
end

reaction_names.each do |reaction_name|
  top_count, top_messages = stats(path, reaction_name)
  puts "#{reaction_name}: #{top_count}"
  puts top_messages.join("\n\n")
  puts "\n#{"*" * 40}\n"
end
