class CreatePages < ActiveRecord::Migration[6.1]
  def change
    create_table :pages do |t|
      t.text :url, null: false, index: { unique: true }
      t.text :parsed_data, null: false
      t.string :file_type, null: false

      t.timestamps
    end
  end
end
