require 'dotenv/load'

Dir[File.join(__dir__, '..', 'app', 'lib', '**', '*.rb')].each { |f| require f }
Dir[File.join(__dir__, '..', 'app', 'models', '**', '*.rb')].each { |f| require f }
Dir[File.join(__dir__, '..', 'app', 'api', '**', '*.rb')].each { |f| require f }

DatabaseConnector.establish_connection

I18n.load_path = Dir[File.join(__dir__, 'locales', '*.yml')]
I18n.default_locale = :en
I18n.backend.load_translations
