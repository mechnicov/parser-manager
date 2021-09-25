require 'rubygems'
require 'bundler/setup'

require 'pg'
require 'dotenv/load'
require_relative 'app/lib/database_connector'

connection_details = DatabaseConnector.configuration

namespace :db do
  desc 'Migrate the database'
  task :migrate do
    ActiveRecord::Base.establish_connection(connection_details)
    ActiveRecord::MigrationContext.new('db/migrate/', ActiveRecord::SchemaMigration).migrate
  end

  desc 'Create the database'
  task :create do
    admin_connection = connection_details.merge('database' => 'postgres', 'schema_search_path' => 'public')
    ActiveRecord::Base.establish_connection(admin_connection)
    ActiveRecord::Base.connection.create_database(connection_details['database'])
    puts %(Database #{connection_details['database']} has created)
  rescue ActiveRecord::DatabaseAlreadyExists
    puts %(Database #{connection_details['database']} already exists)
  end

  desc 'Setup the database'
  task setup: %i[create migrate]

  desc 'Drop the database'
  task :drop do
    admin_connection = connection_details.merge('database' => 'postgres', 'schema_search_path' => 'public')
    ActiveRecord::Base.establish_connection(admin_connection)
    ActiveRecord::Base.connection.drop_database(connection_details['database'])
    puts %(Database #{connection_details['database']} has dropped)
  end
end
