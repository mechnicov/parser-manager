Dir[File.join(__dir__, '..', 'app', 'lib', '**', '*.rb')].each { |f| require f }
Dir[File.join(__dir__, '..', 'app', 'models', '**', '*.rb')].each { |f| require f }
Dir[File.join(__dir__, '..', 'app', 'api', '**', '*.rb')].each { |f| require f }

DatabaseConnector.establish_connection
