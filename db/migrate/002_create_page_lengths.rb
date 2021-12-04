class CreatePageLengths < ActiveRecord::Migration[6.1]
  def change
    create_table :page_lengths do |t|
      t.integer :page_length, null: false
      t.belongs_to :page, null: false, foreign_key: true

      t.timestamps
    end
  end
end
